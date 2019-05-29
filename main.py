#!/bin/python
import curses, traceback, string, os
import time
import mpd
from classes import viewport , Topbar, Commandline, ColorTest, Playlist, Lyrics, Library

#-- Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

#MPD DATA
global client



def main(stdscr):
    #setup for mpd
    # TODO try catch implemetieren
    client = mpd.MPDClient(use_unicode=True)
    client.connect("localhost", 6600)

    #initialize colors
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)


    stdscr.nodelay(1)   #Used to make .getch() not wait for a keysroke

    #create all mainviewclasses
    playlist = Playlist(client)
    lyrics = Lyrics()
    colortest = ColorTest()
    library = Library()

    #setup initial terminalseparation
    height, width = stdscr.getmaxyx()
    topview = viewport(0,0,2,width, Topbar(client))
    mainview= viewport(2,0,height-4,width)
    bottomview = viewport(height-2,0,2,width, Commandline(client))


    global running
    running = True

    curses.curs_set(0)
    stdscr.refresh()
    c = None
    while running:

        #stdscr.erase()
        if c in (curses.KEY_END, ord('!'), ord('q')):
            running = False
        elif c == curses.KEY_RESIZE:
            height, width = stdscr.getmaxyx()
            topview.update_on_resize(0,0,3,width)
            mainview.update_on_resize(3,0,height-5,width)
            bottomview.update_on_resize(height-2,0,2,width)
        elif c == ord('p'):
            mainview.set_content(playlist)
        elif c == ord('c'):
            mainview.set_content(colortest)
        elif c == ord(' '):
            playlist.play_chosen()
        elif c == ord('t'):
            playlist.toggle_pause()
        elif c == curses.KEY_DOWN:
            playlist.move_chosen_up()
        elif c == curses.KEY_UP:
            playlist.move_chosen_down()
        else:
            pass
        topview.render_content()
        mainview.render_content()
        bottomview.render_content()

        topview.display_content()
        mainview.display_content()
        bottomview.display_content()


        c = stdscr.getch()
        time.sleep(0.200)
if __name__=='__main__':
    curses.wrapper(main)

