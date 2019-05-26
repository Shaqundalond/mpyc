import curses
import itertools
import mpd

class viewport():

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
        #needed for Sondata like title and time
        currentsong = self.client.currentsong()
        status = self.client.status()

        #constant data
        logostring =  " MPyC "
        mid_pos = width//2

        #TODO scrolling Text
        #TODO adaptiv removing Paused and MPyC
        #get and define important Data to display
        if status["state"] == "stop":
            songtitle = "No Song playing"
            statestring = "Stopped:"
            mult = 0
        elif status["state"] == "pause":
            statestring = "Paused:"
            songtitle = currentsong["artist"] + " | "+ currentsong["title"]
            time_info = status["time"].split(":")
            percent_per_char = 100/(width-1)
            mult = int((int(time_info[0])/int(time_info[1])*100)/percent_per_char)
        elif status["state"] == "play":
            songtitle = currentsong["artist"] + " | "+ currentsong["title"]
            statestring = "Playing:"
            time_info = status["time"].split(":")
            percent_per_char = 100/(width-3)
            mult = int((int(time_info[0])/int(time_info[1])*100)/percent_per_char)
        else:
            pass


        len_songtitle = len(songtitle)
        progressbar = "="*mult + ">"


        #actual rendering of Topbar
        window.addstr(0,1, statestring, curses.A_BOLD)
        window.addstr(0, mid_pos - len_songtitle//2, songtitle, curses.A_NORMAL)
        window.addstr(0, width - 1 - len(logostring),logostring, curses.A_STANDOUT)

        window.hline(1,0,curses.ACS_HLINE | curses.color_pair(13) ,width)
        window.addstr(1, 0, progressbar,curses.A_BOLD | curses.color_pair(3))

class Commandline():

    def __init__(self, client):

        self.client = client
    def render(self, pos_y, pos_x, height, width, window):

        status = self.client.status()
        if status["state"] == "stop":
            time_elapsed = "x"
            time_song = "x"
        else:
            time_info = status["time"].split(':')

            time_elapsed_min = str(int(time_info[0]) // 60)
            time_elapsed_sec = str(int(time_info[0]) % 60)
            if len(time_elapsed_sec) == 1:
                time_elapsed_sec = "0" + time_elapsed_sec
            time_elapsed = str(time_elapsed_min) + ":" + str(time_elapsed_sec)

            time_song_min = str(int(time_info[1]) // 60)
            time_song_sec = str(int(time_info[1]) % 60)
            if len(time_song_sec) == 1:
                time_song_sec = "0" + time_song_sec
            time_song = time_song_min + ":" + time_song_sec

        songduration = "["+time_elapsed +"|"+ time_song +"]"
        window.hline(0,0,curses.ACS_HLINE | curses.color_pair(13),width)
        window.addstr(0, width - 1 - len(songduration),songduration, curses.A_BOLD | curses.color_pair(3))
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
        self.titlestyle = curses.A_BOLD | curses.color_pair(2)
        self.chosen = curses.A_STANDOUT
        self.not_chosen = curses.A_NORMAL
        self.playlist_position_visual = 0
        self.playlist_position_in_list = 0
        self.playlist_start = 0
        self.window_width = 0
        self.window_height = 0
        self.playlist_length = 0

    def render(self, pos_y, pos_x, height, width, window):
        #Stuff that needs to move into update
        self.window_width = width
        self.window_height = height
        self.playlist_length = self.client.status()["playlistlength"]
        # simple resizing or the resizing of the window
        # TODO more horizontal adaptive scaling to keep more of the Title in Focus
        size_artist = 10
        size_track = 5
        size_album = 6
        size_time = 5
        size_title = width - 1 - (size_artist+1) - (size_track+1) - (size_album+1) - (size_time+1)
        start_pos_track = size_artist + 1
        start_pos_title = start_pos_track + size_track + 1
        start_pos_album = width - 1 - size_time - 1 - size_album
        start_pos_time = width - 1 - size_time
        # Drawing of the Header
        window.addstr(0,0,"Artist",self.titlestyle)
        window.addstr(0,start_pos_track,"Track",self.titlestyle)
        window.addstr(0,start_pos_title,"Title",self.titlestyle)
        window.addstr(0,start_pos_album,"Album",self.titlestyle)
        window.addstr(0,start_pos_time,"Time",self.titlestyle)
        window.hline(1,0,curses.ACS_HLINE | curses.color_pair(13),width)

        #index = 0

        #for song in itertools.islice(self.client.playlistinfo(),self.playlist_start, self.playlist_start + (height - 2)):
        #"ugly" method for only getting enough item as the screen can handle
        for index, song in enumerate(self.client.playlistinfo()[self.playlist_start: self.playlist_start + (height - 2)]):
            # formating of the time for time column
            duration_min = str(int(song["time"]) // 60)
            duration_sec = str(int(song["time"]) % 60)
            if len(duration_sec) == 1:
                duration_sec = "0" + duration_sec
            if len(duration_min) == 1:
                duration_min = " " + duration_min

            duration = str(duration_min) + ":" + str(duration_sec)

            if self.playlist_position_visual == index:
                textstyle = self.chosen
                # simple hack to highlight the whole line_
                # width -1 is needed for god knows why
                # else the player breaks when hightlighting the last line
                window.addstr(index + 2 ,0, " "*(width-1), self.chosen)
                #except:
                #print(index +2 ,"\n" ,self.window_height, "\n", self.playlist_position_visual)

            else:
                textstyle = self.not_chosen

            # actual drawin of the Playlist Text
            window.addstr(index + 2,0,song["artist"][:size_artist],textstyle | curses.color_pair(4))
            window.addstr(index + 2,start_pos_track,song["track"][:size_track], textstyle | curses.color_pair(4))
            window.addstr(index + 2,start_pos_title,song["title"][:size_title],textstyle | curses.color_pair(8))
            window.addstr(index + 2,start_pos_album,song["album"][:size_album],textstyle | curses.color_pair(7))
            window.addstr(index + 2,start_pos_time,duration[:size_time],textstyle | curses.color_pair(6))
            #index +=1

    def move_chosen_up(self):
        if self.playlist_position_visual == self.window_height - 2 and self.playlist_position_in_list == int(self.playlist_length) -1 :
            # two is used because top row 2 takes two rows
            curses.beep()
        elif  self.playlist_position_visual == self.window_height-3:
            self.playlist_position_in_list += 1
            self.playlist_start +=1
        else:
            self.playlist_position_visual +=1

    def move_chosen_down(self):
        self.playlist_position_visual -=1
        self.playlist_position_in_list -= 1


    def play_chosen():
        pass

    def pause():
        pass
