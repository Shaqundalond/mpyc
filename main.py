#!/bin/python
import curses, traceback, string, os
import time
import mpd


#-- Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

#MPD DATA
global client

class viewport:

    def __init__(self, pos_y, pos_x, height, width, content=None):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.height = height
        self.width = width
        self.content = content
        self.screen = curses.newwin(self.height,self.width,self.pos_y,self.pos_x)

    def update_on_resize(self,pos_y, pos_x, height, width):
        self.height = height
        self.width = width
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.screen.resize(self.height,self.width)
        self.screen.mvwin(self.pos_y,self.pos_x)

    def set_content(self, content):
        self.content = content

    def render_content(self):
        self.screen.erase()
        if self.content == None:
            #self.screen.box()
            pass
        else:
            self.content.render(self.pos_y, self.pos_x, self.height, self.width, self.screen)
        self.screen.refresh()


class Topbar:
    def __init__(self, client):
        self.client = client

    def render(self,pos_y,pos_x, height, width, window):
        currentsong = self.client.currentsong()
        status = self.client.status()
        #get and define important Data
        if status["state"] == "stop":
            songtitle = "No Song playing"
            statestring = "Stopped:"
        elif status["state"] == "pause":
            statestring = "Paused:"
            songtitle = currentsong["artist"] + " | "+ currentsong["title"]
        elif status["state"] == "play":
            songtitle = currentsong["artist"] + " | "+ currentsong["title"]
            statestring = "Playing:"
        else:
            pass

        logostring =  " MPyC "
        mid_pos = width//2
        len_songtitle = len(songtitle)
        window.addstr(0,1, statestring, curses.A_BOLD)
        window.addstr(0, mid_pos - len_songtitle//2, songtitle, curses.A_NORMAL)
        window.addstr(0, width - 1 - len(logostring),logostring, curses.A_STANDOUT)
        window.addstr(1, 2, "============>",curses.A_NORMAL)
        window.hline(2,0,curses.ACS_HLINE,width)

class Commandline():

    def __init__(self, client):

        self.client = client
    def render(self, pos_y, pos_x, height, width, window):

        status = self.client.status()
        if status["state"] == "stop":
            time_elapsed = "x"
            time_passed = "x"
        else:
            time_info = status["time"].split(':')
            time_elapsed_min = int(time_info[0]) // 60
            time_elapsed_sec = int(time_info[0]) % 60
            time_elapsed = str(time_elapsed_min) + ":" + str(time_elapsed_sec)

            time_passed_min = int(time_info[1]) // 60
            time_passed_sec = int(time_info[1]) % 60
            time_passed = str(time_passed_min) + ":" + str(time_passed_sec)

        songduration = "["+time_elapsed +"|"+ time_passed +"]"
        window.hline(0,0,curses.ACS_HLINE,width)
        window.addstr(0, width - 1 - len(songduration),songduration, curses.A_NORMAL)
        window.addstr(1 ,1,"lel",curses.A_NORMAL)

class ColorTest():
    def render(self, pos_y, pos_x, height, width, window):
        maxy, maxx = height,width
        maxx = maxx - maxx % 5
        x = 0
        y = 1
        try:
            for i in range(0, curses.COLORS):
                window.addstr(y, x, '{0:5}'.format(i), curses.color_pair(i))
                x = (x + 5) % maxx
                if x == 0:
                    y += 1
        except:
            pass
        window.addstr(0,width//2, "Playlist", curses.color_pair(curses.COLOR_BLUE))

class Library():
    pass

class Lyrics():
    pass

class Playlist():
    def __init__(self, client):
        self.client = client
        self.titletext = curses.A_BOLD | curses.color_pair(2)

    def render(self, pos_y, pos_x, height, width, window):
        size_artist = 10
        size_track = 5
        size_album = 6
        size_time = 5
        size_title = width -1 - size_artist - size_track - size_album - size_time
        start_pos_track = size_artist + 1
        start_pos_title = start_pos_track + size_track + 1
        start_pos_album = width - 1 - size_time - 1 - size_album
        start_pos_time = width - 1 - size_time

        window.addstr(0,0,"Artist",self.titletext)
        window.addstr(0,start_pos_track,"Track",self.titletext)
        window.addstr(0,start_pos_title,"Title",self.titletext)
        window.addstr(0,start_pos_album,"Album",self.titletext)
        window.addstr(0,start_pos_time,"Time",self.titletext)
        window.hline(1,0,curses.ACS_HLINE,width)

        for index, lel in enumerate(self.client.playlistinfo()):
            window.addstr(index + 2,0,lel["artist"][:size_album],curses.A_NORMAL)
            window.addstr(index + 2,start_pos_track,lel["track"][:size_track], curses.A_NORMAL)
            window.addstr(index + 2,start_pos_title,lel["title"][:size_title],curses.A_NORMAL)
            window.addstr(index + 2,start_pos_album,lel["album"][:size_album],curses.A_NORMAL)
            window.addstr(index + 2,start_pos_time,lel["time"][:size_time],curses.A_NORMAL)


def main(stdscr):
    #setup for mpd
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
    topview = viewport(0,0,3,width, Topbar(client))
    mainview= viewport(3,0,height-5,width)
    bottomview = viewport(height-2,0,2,width, Commandline(client))


    global running
    running = True

    curses.curs_set(0)
    stdscr.refresh()
    while running:
        c = stdscr.getch()

        #stdscr.erase()
        if c in (curses.KEY_END, ord('!'), ord('q')):
            running = False
        if c == ord('p'):
            mainview.set_content(playlist)
        if c == ord('c'):
            mainview.set_content(colortest)
        elif c == curses.KEY_RESIZE:
            height, width = stdscr.getmaxyx()
            topview.update_on_resize(0,0,3,width)
            mainview.update_on_resize(3,0,height-5,width)
            bottomview.update_on_resize(height-2,0,2,width)

        else:
            pass
        topview.render_content()
        mainview.render_content()
        bottomview.render_content()
        time.sleep(0.100)
if __name__=='__main__':
    curses.wrapper(main)

