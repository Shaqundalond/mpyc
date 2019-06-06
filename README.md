# mpyc
A "simple" curses mpd client written in Python. It is a spiritual copy of ncmcpp. Right now it has only been tested under linux.

![MPyC](/img/mpyc.jpg)


# Requirements
## Python3
For this to work right now you need to have the module pyhton-mpd2 installed on your System
```Bash
pip3 install pyhton-mpd2
```
In some cases pip needs the --user flag to properly install the module

##MPD
mpyc uses mpd as daemon. MPD must be installed. For Debian-based systems run

```Bash
sudo apt-get update
sudo apt-get install mpd
```
MPD needs to be configured and running for mpyc to function properly. A sample config can be found in docs. This config needs to be saved under $HOME/.config/mpd.

(Optional)To enable MPD on every systemstart run following command assuming you use systemd.

```Bash
sudo systemctl enable mpd.service
```
To start MPD run following command assuming you use systemd

```Bash
sudo systemctl start mpd.service
```

# TODO
## Allgemein
* Update Funktion
* Abfangen falls MPD nicht läuft

## MPD
* MPD abspielen
* MPD Playlist auslesen [done]

## curses
* HOTKEYS definieren
* Klassen definieren fuer:
	[done]Playlist x
	[done]Library x
	[done]Visualizer x
	[done]Statusbar x
	[done]Bottombar x

## Statusbar
* Current Song:
	[done]benoetigt Time
	[done]nimm Song String und schneide ihn mit [n:k] ab
	[done]aktualisiere n und k nach X ticks
	[done]k-n = width - reservierte Zeichen  (MpYC z.B)
	Song titel als Laufschrift realisieren
* Progress in Song:
	100/width = % per width_unit


## Bottombar
* commandline


## Playlist
* Playlist anzeigen:
	* farbliches Highlighten
	* [deprecated] Scrollbar falls Playlist > window.height
	* [done] Highlighting auf welchem Song ich bin

* Playlist elemete loeschen
* Playlist Elemente verschieben
* Anpassen dass width/height per extrafunktion geupdatet wird
* anzeigen von Bildern mittels Ueberzug
*





## Library
* Library anzeigen
* add Element to playlist
* highlight multiple Elements
* recursive Adding to playlist


## Keyhandler
* muss zwischen den Fenstern unterscheiden können
* q for quit


