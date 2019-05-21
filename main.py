#!/bin/python
import curses, traceback, string, os
import time


#-- Define the appearance of some interface elements
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

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
            self.screen.box()
        else:
            self.content.render(self.pos_y, self.pos_x, self.height, self.width, self.screen)
        self.screen.refresh()


class Topbar():

    def render(self,pos_y,pos_x, height, width, window):
        songtitle = "Beispiel Songtitel der nicht Scrollt"
        logostring =  " MPyC "
        mid_pos = width//2
        len_songtitle = len(songtitle)
        window.addstr(0, mid_pos - len_songtitle//2, songtitle, curses.A_NORMAL)
        window.addstr(0, width - 1 - len(logostring),logostring, curses.A_STANDOUT)
        window.addstr(1, 2, "============>",curses.A_NORMAL)
        window.hline(2,0,curses.ACS_HLINE,width)

class Commandline():
    def render(self, pos_y, pos_x, height, width, window):
        #window.box()
        songduration = "[1:25|3:33]"
        window.hline(0,0,curses.ACS_HLINE,width)
        window.addstr(0, width - 1 - len(songduration),songduration, curses.A_NORMAL)
        window.addstr(1 ,1,"lel",curses.A_NORMAL)

class Playlist():
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

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    stdscr.nodelay(1)   #Used to make .getch() not wait for a keysroke
    height, width = stdscr.getmaxyx()
    topview = viewport(0,0,3,width, Topbar())
    mainview= viewport(3,0,height-5,width,Playlist())
    bottomview = viewport(height-2,0,2,width, Commandline())
    global running
    running = True

    curses.curs_set(0)
    stdscr.refresh()
    while running:
        c = stdscr.getch()

        #stdscr.erase()
        if c in (curses.KEY_END, ord('!'), ord('q')):
            running = False
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
        time.sleep(0.033)
if __name__=='__main__':
    curses.wrapper(main)

