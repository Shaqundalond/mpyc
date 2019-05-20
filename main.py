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

        logostring =  " MPyC "
        window.addstr(1, width - 1 - len(logostring),logostring, curses.A_STANDOUT)
        window.addstr(2, 2, "-------------->",curses.A_NORMAL)
        window.box()

class Commandline():
    def render(self, pos_y, pos_x, height, width, window):
        window.box()
        window.addstr(1 ,1,"lel",curses.A_NORMAL)



def main(stdscr):
    stdscr.nodelay(1)   #Used to make .getch() not wait for a keysroke
    height, width = stdscr.getmaxyx()
    topview = viewport(0,0,4,width, Topbar())
    mainview= viewport(4,0,height-7,width)
    bottomview = viewport(height-3,0,3,width, Commandline())
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
            topview.update_on_resize(0,0,4,width)
            mainview.update_on_resize(4,0,height-7,width)
            bottomview.update_on_resize(height-3,0,3,width)

        else:
            pass
        topview.render_content()
        mainview.render_content()
        bottomview.render_content()
        #stdscr.refresh()

if __name__=='__main__':
    curses.wrapper(main)

