#!/bin/python
import curses, traceback, string, os
import time
import mpd
import threading
from classes import viewport , Topbar, Commandline, ColorTest, Playlist, Lyrics, Library, Help


def main(stdscr):
    # Define functions used by keyhandler.
    # Yes it is a makeshift class that I tried to prevent to reate...
    def terminate():
        nonlocal running
        running = False


    def resize():
        nonlocal height, width, topview, mainview, bottomview, stdscr
        height, width = stdscr.getmaxyx()
        topview.update_on_resize(0,0,3,width)
        mainview.update_on_resize(3,0,height-5,width)
        bottomview.update_on_resize(height-2,0,2,width)


    def to_library():
        nonlocal library, mainview,  d_functionkeys_window
        d_functionkeys_window = library.get_keys()
        playlist.get_playlist()
        mainview.set_content(library)


    def to_playlist():
        nonlocal playlist, mainview, d_functionkeys_window
        d_functionkeys_window = playlist.get_keys()
        playlist.get_playlist()
        mainview.set_content(playlist)


    def to_help():
        mainview.set_content(help_screen)



    def volume_up():
        nonlocal client, bottomview
        status = client.status()
        if "volume" in client.status():
            vol = int(status["volume"])
            if vol <=95:
                 vol += 5
            if vol >95:
                vol = 100
            client.setvol(vol)
            message = "Volume set to: " + str(vol) + "%"
        else:
            message = "Can't set Volume, no softwaremixer available"
        bottomview.content.display(message)


    def volume_down():
        nonlocal client, bottomview
        status = client.status()
        if "volume" in client.status():
            vol = int(status["volume"])
            if vol >=5:
                 vol -= 5
            if vol <5:
                vol = 0
            client.setvol(vol)
            message = "Volume set to: " + str(vol) + "%"
        else:
            message = "Can't set Volume, no softwaremixer available"
        bottomview.content.display(message)


    def next_song():
        if client != None:
            client.next()


    def prev_song():
        if client != None:
            client.previous()


    def random():
        if client != None:
            a = bottomview.content.update_playback(0x2)
            client.random(1) if a else client.random(0)


    def consume():
        if client != None:
            a = bottomview.content.update_playback(0x8)
            client.consume(1) if a else client.consume(0)


    def single():
        if client != None:
            a = bottomview.content.update_playback(0x4)
            client.single(1) if a else client.single(0)


    def repeat():
        if client != None:
            a =bottomview.content.update_playback(0x1)
            client.repeat(1) if a else client.repeat(0)


    def search():
        x.start()
        #x.join()


    #################
    # Setup for mpd #
    #################
    try:
        client = mpd.MPDClient(use_unicode=True)
        client.connect("localhost", 6600)       # The socket is hardcoded and should rather be read from config file.
    except:
        client = None


    ############################
    # Setup  Curses and Colors #
    ############################

    curses.start_color()
    curses.use_default_colors()
    # initialize all colors because I'm lazy
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    curses.curs_set(0)      # Hide The cursor
    stdscr.nodelay(1)       #Used to make .getch() not wait for a keysroke
    curses.halfdelay(1)     # make curses.getch() wait for 1/10 second until returning None
    stdscr.refresh()        # clear the screen for initial setup
    c = None                # Iniitalize c for keystrokes
    height, width = stdscr.getmaxyx()


    ######################
    # Initialize Classes #
    ######################
    help_screen = Help()
    playlist = Playlist(client)
    lyrics = Lyrics()
    colortest = ColorTest()
    library = Library(client)

    topview = viewport(0,0,2,width, Topbar(client))
    mainview= viewport(2,0,height-4,width, help_screen)
    bottomview = viewport(height-2,0,2,width, Commandline(client))

    # Ugly thread for keyinput
    x = threading.Thread(target=bottomview.content.get_input ,args = (height, width))

    ####################
    # Setup Keyhandler #
    ####################

    # The dictionaries store the adresses of the functions
    # That will be called on Keypress
    d_functionkeys_main = {
            ord('q') : terminate,
            curses.KEY_RESIZE : resize,
            # Movement controls
            ord('1') : to_playlist,
            ord('2') : to_library,
            ord('3') : to_help,
            #General Musicplayer controls
            ord('p') : playlist.toggle_pause,
            ord('+') : volume_up,
            ord('-') : volume_down,
            ord('>') : next_song,
            ord('<') : prev_song,
            ord('r') : random,
            ord('c') : consume,
            ord('s') : single,
            ord('w') : repeat,
            ord('/') : search,
            #ord('u') : update
            }

    d_functionkeys_window = {}


    ############
    # Mainloop #
    ############
    #counter = 0
    running = True
    while running:
        #"KEYHANDLER"
        keypressed = True # Boolean to store valid keypress

        if c in d_functionkeys_main:
            d_functionkeys_main[c]()
        elif c in d_functionkeys_window:
            d_functionkeys_window[c]()
        else:
            keypressed = False

        # Renderpart
        topview.render_content()
        mainview.render_content()
        bottomview.render_content()

        # Display the rendered buffer to the terminal
        topview.display_content()
        mainview.display_content()
        bottomview.display_content()


        c = stdscr.getch() #get pressed Key
        curses.flushinp() # Flush input to make curses store only one keystroke
        if not keypressed:
            # sleep for 1/25 second to minimize processor load
            curses.napms(40)


if __name__=='__main__':
    #Inbuilt wrapper function to prevent garbling up the terminal
    curses.wrapper(main)

