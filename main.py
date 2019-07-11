#!/bin/python
import curses, traceback, string, os
import time
import mpd
from classes import viewport , Topbar, Commandline, ColorTest, Playlist, Lyrics, Library

#-- Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

#MPD DATA
#global client



def main(stdscr):
    running = True
    # Define functions for easier keyhandling.
    # Yes it is a makeshift class that I tried to prevent...
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




    #setup for mpd
    # TODO try catch implemetieren
    try:
        client = mpd.MPDClient(use_unicode=True)
        client.connect("localhost", 6600)       # The socket is hardcoded and should rather be read from config file.
    except:
        client = None

    #initialize colors
    curses.start_color()
    curses.use_default_colors()
    # initialize all colors because I'm lazy
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)


    stdscr.nodelay(1)   #Used to make .getch() not wait for a keysroke

    #create all mainviewclasses
    playlist = Playlist(client)
    lyrics = Lyrics()
    colortest = ColorTest()
    library = Library(client)

    #setup initial terminalseparation
    height, width = stdscr.getmaxyx()
    topview = viewport(0,0,2,width, Topbar(client))
    mainview= viewport(2,0,height-4,width)
    bottomview = viewport(height-2,0,2,width, Commandline(client))




    curses.curs_set(0)      # Hide The cursor
    curses.halfdelay(1)     # make curses.getch() wait for 1/10 of a second until returning None
    stdscr.refresh()        # clear the screen for initial setup
    c = None                # Iniitalize c for keystrokes
    d_functionkeys_main = {
            ord('q'):terminate,
            curses.KEY_RESIZE:resize,
            ord('1'):to_playlist,
            ord('2'):to_library,
            ord('p'):playlist.toggle_pause,
            ord('+'):volume_up,
            ord('-'):volume_down

            }
    #d_functionkeys = d_functionkeys_main # workaround to append other dictionaries to the main one
    d_functionkeys_window = {}
    #Mainloop
    while running:
        #"KEYHANDLER"
        # TODO cleanup for different windows
        keypressed = True # Boolean to store valid keypress

        if c in d_functionkeys_main:
            d_functionkeys_main[c]()
        elif c in d_functionkeys_window:
            d_functionkeys_window[c]()
        else:
            keypressed = False

        # Renderpart
        topview.render_content()
        if keypressed:
            #mainview gets only updated on keypress
            mainview.render_content()
        bottomview.render_content()

        # Display the rendered buffer to the terminal
        topview.display_content()
        if keypressed:
            mainview.display_content()
        bottomview.display_content()


        c = stdscr.getch() #get pressed Key
        curses.flushinp() # Flush input to make curses store only one keystroke
        if not keypressed:
            # sleep for 1/10 second to minimize processor load
            curses.napms(100)


if __name__=='__main__':
    #Inbuilt wrapper function to prevent garbling up the terminal
    curses.wrapper(main)

