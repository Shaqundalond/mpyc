# mpyc
A "simple" curses mpd client written in Python. It is a spiritual copy of ncmcpp. Right now it has only been tested under linux.

![MPyC](/img/mpyc.jpg)

# Abilities
## Basic Abilities
* Display current Playlist
* Acessing Library
* Basic Media control:
	* Play Pause Stop
	* Shuffle
	* Volume Control

## Nice to have Abilities
* Visualizer
* Fetching Lyrics
* Displaying Album Cover (Only in Terminal Emulator)


# Requirements
## Python3
For this to work right now you need to have the module pyhton-mpd2 installed on your System
```Bash
pip3 install pyhton-mpd2
```
In some cases pip needs the --user flag to properly install the module

## MPD
mpyc uses mpd as daemon. MPD must be installed. For Debian-based systems run

```Bash
sudo apt-get update
sudo apt-get install mpd
```
MPD needs to be configured and running for mpyc to function properly. A sample config can be found in docs. This config needs to be saved under $HOME/.config/mpd. Make sure that the Music Directory used in your mpd.conf contains music files.

(Optional)To enable MPD on every systemstart run following command assuming you use systemd.

```Bash
sudo systemctl enable mpd.service
```
To start MPD run following command assuming you use systemd

```Bash
sudo systemctl start mpd.service
```

# First Usage
When using MPD for the first time after opening MPyC press "u" to update your Music Database. MPD will now update its Database. Depending on the size of your Library this may take a while. MPyC always starts on the helpscreen with its keybindings.

# Tasks
## General
- [ ] Update function for mpd
- [x] catch if mpd is not running
- [x] Volume Control

## Library
- [ ] query Library:
	- [ ] search for specific Items
- [x] display Library
- [x] add Folder to Playlist

## Bottombar
- [ ] implement Commandmode:
	- [ ] Search (Dependend on what Screen is showing)
	- [ ]


## Playlist
- [x] make current Song bold

## Keyhandler
- [x] implement Keyhandler
- [x] implement Keybindings (Vim)

## Known Problems
- [ ] Playlist does not get updated/refreshed automatically
