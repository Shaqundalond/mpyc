# mpyc
A "simple" curses media player client written in Python

# TODO


## MPD
*MPD abspielen
*MPD Playlist auslesen

## curses
* HOTKEYS definieren
* Klassen definieren fuer:
	Playlist x
	Library x
	Visualizer x
	Statusbar x
	Bottombar x

## Statusbar
* Current Song:
	benoetigt Time
	nimm Song String und schneide ihn mit [n:k] ab
	aktualisiere n und k nach X ticks
	k-n = width - reservierte Zeichen  (MpYC z.B)
* Progress in Song:
	100/width = % per width_unit


## Bottombar
* q for quit

## Playlist
* Playlist anzeigen:
	* farbliches Highlighten
	* Scrollbar falls Playlist > window.height
	* Highlighting auf welchem Song ich bin

* Playlist elemete loeschen
* Playlist Elemente verschieben

## Library
* Library anzeigen
* add Element to playlist
* highlight multiple Elements
* recursive Adding to playlist


Keyhandler


