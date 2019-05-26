# mpyc
A "simple" curses media player client written in Python

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


