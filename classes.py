import curses
import itertools
import mpd

class viewport():

    def __init__(self, pos_y, pos_x, height, width, content=None):
        '''
        The Coordinates used for curses use the coordinate
        system established by cathode ray tubes.
        X gets bigger from left to right
        Y gets bigger from top to bottom
        Upper left corner is (0/0)
        '''
        self.pos_y = pos_y      #y Coordinate in the terminal
        self.pos_x = pos_x      #x Coordinate in the terminal
        self.height = height
        self.width = width
        self.content = content  # Variable used to store the crrent class that is displayed
        self.content_name = content.__class__.__name__
        self.screen = curses.newwin(self.height,self.width,self.pos_y,self.pos_x) # create new sudwindow to draw to.

    def update_on_resize(self,pos_y, pos_x, height, width):
        '''
        function used to resize and move the window to the proper new positions after the terminal gets resize
        '''
        self.height = height
        self.width = width
        self.pos_y = pos_y
        self.pos_x = pos_x

        # curses function to update the screen
        self.screen.resize(self.height,self.width)
        self.screen.mvwin(self.pos_y,self.pos_x)

    def set_content(self, content):
        '''
        function used for changing the content of the view (ntil now only used for mainview)
        '''
        self.content = content

    def render_content(self):
        # clear the screen to prevent artifacts from last frame
        self.screen.erase()
        if self.content == None:
            #self.screen.box()
            pass
        else:
            self.content.render(self.pos_y, self.pos_x, self.height, self.width, self.screen)

    def display_content(self):
        self.screen.refresh()


class Topbar:
    def __init__(self, client):
        self.client = client

    def render(self,pos_y,pos_x, height, width, window):
        #constant data
        logostring =  " MPyC "
        mid_pos = width//2

        #initial check if client is up
        if self.client == None:
            window.addstr(0,3 ,"Client not running", curses.A_BLINK)
            window.addstr(0, width - 1 - len(logostring),logostring, curses.A_STANDOUT)
            window.hline(1,0,curses.ACS_HLINE | curses.color_pair(13) ,width)
            return

        #needed for Songdata like title and time
        currentsong = self.client.currentsong()
        status = self.client.status() # dicitonary with a lot of useful information

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
            percent_per_char = 100/(width-1)
            mult = int((int(time_info[0])/int(time_info[1])*100)/percent_per_char)
        else:
            pass

        songtitle = songtitle[:width]
        len_songtitle = len(songtitle)
        progressbar = "="*mult + ">"


        #actual rendering of Topbar
        window.addstr(0,1, statestring, curses.A_BOLD)
        window.addstr(0, mid_pos - len_songtitle//2, songtitle, curses.A_NORMAL)
        window.addstr(0, width - 1 - len(logostring),logostring, curses.A_STANDOUT)

        window.hline(1,0,curses.ACS_HLINE | curses.color_pair(13) ,width)
        #[:width] is used to prevent pointer out of range
        window.addstr(1, 0, progressbar[:width-1],curses.A_BOLD | curses.color_pair(3))

class Commandline():

    def __init__(self, client):

        self.client = client
        self.message = "" # String used to display Data from keystrokes
        tmp_status = self.client.status()
        tmp_playback = [tmp_status["repeat"],tmp_status["random"],tmp_status["single"],tmp_status["consume"]]
        tmp_shifter = 0x1
        self.playback_array = ['w','r','s','c'] # LSB is left

        #This is for me to use bitshifting
        #consume(c)-single(s)-random(r)repeat(w) LSB is right
        self.playback = 0x0
        for x in tmp_playback:
            if x == "1":
                self.playback ^= tmp_shifter
            tmp_shifter <<= 1



    def render(self, pos_y, pos_x, height, width, window):

        #initial check if client is up
        if self.client == None:
            window.addstr(1,3 ,"Client not running", curses.A_BLINK)
            window.hline(0,0,curses.ACS_HLINE | curses.color_pair(13),width)
            return


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

        tmp_playback  = self.playback
        s_playback = "["
        for i in self.playback_array:
            if tmp_playback & 0x1 == 0x1:
                s_playback += i
            else:
                s_playback += "-"
            tmp_playback >>= 1

        s_playback += "]"



        window.hline(0,0,curses.ACS_HLINE | curses.color_pair(13),width)
        window.addstr(0, width - 1 - len(songduration),songduration, curses.A_BOLD | curses.color_pair(3)) #Songduration
        window.addstr(0, 2, s_playback, curses.A_BOLD | curses.color_pair(3))

        if len(self.message) >= width -1:
            self.message = self.message[:width-5] + "..."
        window.addstr(1 ,1,self.message,curses.A_NORMAL)

    def display(self, text):
        self.message = text

    def update_playback(self, a):
        self.playback ^= a
        return int(self.playback & a)


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
    def __init__(self, client):
        self.client = client
        self.titlestyle = curses.A_BOLD | curses.color_pair(2)
        self.chosen = curses.A_STANDOUT
        self.not_chosen = curses.A_NORMAL

        # for current directory
        self.directory_position_visual = 0          # position on the list displayed on screen [0..height]
        self.directory_position_in_list = 0         # actual position in the queried list
        self.directory_start = 0                    # position needed to offset the returned directory_list

        self.l_directory_position_store = []
        ''' contains
        [0]self.uri
        [1]self.uri_last
        [2]self.directory_position_visual
        [3]self.directory_position_in_list
        [4]self.directory_start
        as list to restore these values when traversing the directory-tree
        '''
        self.window_width = 0
        self.window_height = 0
        self.directory_length = 0
        self.uri = ""
        self.uri_last = None
        self.directory = None


        self.d_keys = {
            #Arrow keys
            curses.KEY_UP : self.move_chosen_down,
            curses.KEY_DOWN : self.move_chosen_up,
            curses.KEY_RIGHT : self.enter_directory,
            curses.KEY_LEFT : self.return_directory,
            curses.KEY_ENTER : self.add_directory,
            #VIM Keys
            ord('j') : self.move_chosen_up,
            ord('k') : self.move_chosen_down,
            ord('l') : self.enter_directory,
            ord('h') : self.return_directory,
            ord(' ') : self.add_directory
            }


    def render(self, pos_y, pos_x, height, width, window):

        #Stuff that needs to move into update
        self.window_width = width
        self.window_height = height

        if self.client == None:
            self.directory_list = []
        elif self.uri != "":
            self.directory_list = [{"directory": ".." } ] + self.client.lsinfo(self.uri)
        else:
            self.directory_list =  self.client.lsinfo(self.uri)


        self.directory_length = len(self.directory_list)


        #"ugly" method for only getting enough item as the screen can handle
        for index, library_item in enumerate(self.directory_list[self.directory_start: self.directory_start + height], 0):

            a = 2
            b= 3
            if "directory" in library_item:
                item = "[ " + library_item["directory"] + " ]"
                #TODO Splice

            elif "file" in library_item:
                item = library_item["file"]

            else:
                item = "WTF"

            if self.directory_position_visual == index:
                textstyle = self.chosen
            else:
                textstyle = self.not_chosen
            window.addstr(index,2, item, textstyle | curses.color_pair(2))
            # ,textstyle | curses.color_pair(4))



    def move_chosen_up(self):
        #check if last item is highlighted
        if self.directory_position_in_list == int(self.directory_length) - 1:
            # do nothing
            curses.beep()
        # check if last item is visually reached
        elif  self.directory_position_visual == self.window_height-1:
            self.directory_position_in_list += 1 #move to next item in array
            self.directory_start +=1 #shift visual directory
        # move "pointer" visually in array and visual further
        else:
            self.directory_position_visual +=1
            self.directory_position_in_list +=1

    def move_chosen_down(self):
        #check if first item is highlighted
        if self.directory_position_in_list == 0:
            # do nothing
            curses.beep()
        # check if last item is visually reached
        elif  self.directory_position_visual == 0:
            self.directory_position_in_list -= 1 #move to next item in array
            self.directory_start -=1 #shift visual directory
        # move "pointer" visually in array and visual further
        else:
            self.directory_position_visual -=1
            self.directory_position_in_list -=1
    def return_directory(self):
        if len(self.l_directory_position_store) != 0:
            # restore old lists
            last_directory = self.l_directory_position_store.pop()
            self.uri = last_directory[0]
            self.uri_last = last_directory[1]
            self.directory_position_visual = last_directory[2]
            self.directory_position_in_list = last_directory[3]
            self.directory_start = last_directory[4]

    def enter_directory(self):
        #tmp used to keep my frigging long variable names shorter...
        tmp = self.directory_list[self.directory_position_in_list]
        if "directory" in tmp:
            if tmp["directory"] == "..":
                self.return_directory()
            else:
                #Storing stuff
                a = [self.uri, self.uri_last, self.directory_position_visual ,self.directory_position_in_list, self.directory_start]
                self.l_directory_position_store.append(a)

                self.directory_position_visual = 0
                self.directory_position_in_list = 0
                self.directory_start = 0
                self.uri_last = self.uri
                self.uri = tmp["directory"]

    def add_directory(self):
        tmp = self.directory_list[self.directory_position_in_list]
        if "directory" in tmp:
            # for people like me who press the wrong key... FeelsBadMan
            if tmp["directory"] == "..":
                self.enter_directory()
            item = tmp["directory"]
            self.client.add(item)

            return "Added : " + item
        elif "file" in tmp:
            item = tmp["file"]
            self.client.add(item)
            return "Added : " + item

        else:
            return "Coulnd't add item sometheing went wrong"

    def get_keys(self):
        return self.d_keys


class Lyrics():
    pass

class Playlist():
    def __init__(self, client):
        self.client = client
        self.titlestyle = curses.A_BOLD | curses.color_pair(2)
        self.chosen = curses.A_STANDOUT
        self.not_chosen = curses.A_NORMAL
        self.current =  curses.A_BOLD
        self.playlist_position_visual = 0
        self.playlist_position_in_list = 0
        self.playlist_start = 0
        self.window_width = 0
        self.window_height = 0
        self.s_playlist_length = 0
        self.l_playlist = None
        self.d_keys = {
                 curses.KEY_UP:self.move_chosen_down,
                 curses.KEY_DOWN:self.move_chosen_up,
                 ord('\n') : self.play_chosen,
                 ord(' ') : self.play_chosen,
                 ord('d') : self.delete_chosen
                 # maybe move
                }

    def render(self, pos_y, pos_x, height, width, window):

        #Stuff that needs to move into update to reduce CPU Load
        self.window_width = width
        self.window_height = height
        if self.client != None:
            self.l_client_status = self.client.status()
            self.s_playlist_length = self.l_client_status["playlistlength"]
            if int(self.s_playlist_length) > 0:
                try:
                    self.i_current_song = int(self.l_client_status["song"])
                except:
                    self.i_current_song = -1

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

        # Drawing of the Header in the table€ý,€ý,
        window.addstr(0,0,"Artist",self.titlestyle)
        window.addstr(0,start_pos_track,"Track",self.titlestyle)
        window.addstr(0,start_pos_title,"Title",self.titlestyle)
        window.addstr(0,start_pos_album,"Album",self.titlestyle)
        window.addstr(0,start_pos_time,"Time",self.titlestyle)
        window.hline(1,0,curses.ACS_HLINE | curses.color_pair(13),width)
        # End of stuff that needs to move into update

        #"ugly" method for only getting enough item as the screen can handle
        for index, song in enumerate(self.l_playlist[self.playlist_start: self.playlist_start + (height - 2)], 0):
            #song is returned as dictionary
            # formating of the time for time column
            duration_min = str(int(song["time"]) // 60)
            duration_sec = str(int(song["time"]) % 60)
            if len(duration_sec) == 1:
                duration_sec = "0" + duration_sec
            if len(duration_min) == 1:
                duration_min = " " + duration_min

            duration = str(duration_min) + ":" + str(duration_sec)


            #check if Song Data is complete else replace it with ugly NULL
            if "artist" in song:
                artist = song["artist"]
            else:
                artist = "<NULL>"

            if "track" in song:
                track = song["track"]
                if len(track) == 1:
                    track = "0" + track
            else:
                track = "XX"

            if "title" in song:
                title = song["title"]
            else:
                title = song["file"].split("/")[-1]

            if "album" in song:
                album = song["album"]
            else:
                album = "<NULL>"

            # resetting Textstyle to XOR later
            textstyle = curses.A_NORMAL

            #setting the highlighting
            if (index + self.playlist_start) == self.i_current_song:
                textstyle = textstyle | self.current

            if self.playlist_position_visual == index:
                textstyle = textstyle | self.chosen
                # simple hack to highlight the whole line_
                # width -1 is needed for god knows why
                # else the player breaks when hightlighting the last line
                window.addstr(index + 2 ,0, " "*(width-1), self.chosen)


            # actual drawing of the Playlist Text
            window.addstr(index + 2,0, artist \
                    [:size_artist],textstyle | curses.color_pair(4))
            window.addstr(index + 2,start_pos_track, track  \
                    [:size_track], textstyle | curses.color_pair(4))
            window.addstr(index + 2,start_pos_title, title  \
                    [:size_title],textstyle | curses.color_pair(8))
            window.addstr(index + 2,start_pos_album, album \
                    [:size_album],textstyle | curses.color_pair(7))
            window.addstr(index + 2,start_pos_time,duration[:size_time] \
                    ,textstyle | curses.color_pair(6))



    def move_chosen_up(self):
        #check if last item is highlighted
        if self.playlist_position_in_list == int(self.s_playlist_length) - 1:
            # do nothing
            curses.beep()
        # check if last item is visually reached
        elif  self.playlist_position_visual == self.window_height-3:
            self.playlist_position_in_list += 1 #move to next item in array
            self.playlist_start +=1 #shift visual playlist
        # move "pointer" visually in array and visual further
        else:
            self.playlist_position_visual +=1
            self.playlist_position_in_list +=1

    def move_chosen_down(self):
        #check if first item is highlighted
        if self.playlist_position_in_list == 0:
            # do nothing
            curses.beep()
        # check if last item is visually reached
        elif  self.playlist_position_visual == 0:
            self.playlist_position_in_list -= 1 #move to next item in array
            self.playlist_start -=1 #shift visual playlist
        # move "pointer" visually in array and visual further
        else:
            self.playlist_position_visual -=1
            self.playlist_position_in_list -=1


    def play_chosen(self):
        self.client.play(self.playlist_position_in_list)

    def delete_chosen(self):
        self.client.delete(self.playlist_position_in_list)
        self.l_playlist = self.client.playlistinfo()

    def toggle_pause(self):
        status = self.client.status()["state"]
        #pause play stop
        if status == "pause":
            self.client.pause(0)
        elif status == "play":
            self.client.pause(1)

    def stop():
        pass

    def get_playlist(self):
        if self.client == None:
            self.l_playlist = []
        else:
            self.l_playlist = self.client.playlistinfo()

    def get_keys(self):
        return self.d_keys
