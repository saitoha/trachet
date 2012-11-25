#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012  Hayaki Saito <user@zuse.jp>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ***** END LICENSE BLOCK *****

_SEQDB = {
    '> ESC P<ST>'    : 'DCS',
    '> ESC ]<ST>'    : 'OSC',
    '> ESC ^<ST>'    : 'PM',
    '> ESC _<ST>'    : 'APC',
    '> ESC X<ST>'    : 'SOS',
    '< CSI [0]M'     : 'xterm normal mouse reporting, following 3 bytes mean (code, row, col)',
    '< CSI M'        : 'URXVT (1015) mouse reporting (code, row, col)',
    '< CSI [3]M'     : 'URXVT (1015) mouse reporting (code, row, col)',
    '< CSI <[3]M'    : 'SGR (1006) mouse reporting (code, row, col)',
    '< CSI <M'       : 'SGR (1006) mouse reporting (code, row, col)',
    '< CSI <[3]m'    : 'SGR (1006) mouse reporting, button up (code, row, col)',
    '< CSI <m'       : 'SGR (1006) mouse reporting, button up (code, row, col)',
    '< CSI [3]R'     : 'DSR-DECXCPR(cursor position report) response, DEC specific format',
    '< CSI [2]R'     : 'DSR-CPR(cursor position report) response',
    '< CSI R'        : 'DSR-CPR(cursor position report) response',
    '< CSI 0n'       : 'DSR-OS(operating status report) response: "good status"',
    '< CSI 3n'       : 'DSR-OS(operating status report) response: "it has a malfunction"',
    '< CSI ?c'       : 'DA1 Response',
    '< CSI >c'       : 'DA2 Response',
    '< CSI 15~ '     : 'F5 key (xterm)',
    '< CSI 17~ '     : 'F6 key (xterm)',
    '< CSI 18~ '     : 'F7 key (xterm)',
    '< CSI 19~ '     : 'F8 key (xterm)',
    '< CSI 20~ '     : 'F9 key (xterm)',
    '< CSI 21~ '     : 'F10 key (xterm)',
    '< CSI 23~ '     : 'F11 key (xterm)',
    '< CSI 24~ '     : 'F12 key (xterm)',
    '> ESC 6'        : 'DECBI',
    '> ESC 7'        : 'DECSC',
    '> ESC 8'        : 'DECRC',
    '> ESC 9'        : 'DECFI',
    '> ESC ='        : 'DECKPAM',
    '> ESC >'        : 'DECKPNM',
    '> ESC <SP>F'    : 'S7C1T',
    '> ESC <SP>G'    : 'S8C1T',
    '> ESC <SP>L'    : 'Set ANSI conformance level 1',
    '> ESC <SP>M'    : 'Set ANSI conformance level 2',
    '> ESC <SP>N'    : 'Set ANSI conformance level 3',
    '> ESC #3'       : 'DECDHLT',
    '> ESC #4'       : 'DECDHLB',
    '> ESC #5'       : 'DECSWL',
    '> ESC #6'       : 'DECDWL',
    '> ESC #8'       : 'DECALN',
    '> ESC %@'       : 'Select default character set',
    '> ESC %G'       : 'Select UTF-8 character set',
    '> ESC (0'       : 'designate G0 charset: DEC Special Character and Line Drawing Set',
    '> ESC (A'       : 'designate G0 charset: United Kingdom (UK)',
    '> ESC (B'       : 'designate G0 charset: United States (USASCII)',
    '> ESC (4'       : 'designate G0 charset: Dutch',
    '> ESC (C'       : 'designate G0 charset: Finnish',
    '> ESC (5'       : 'designate G0 charset: Finnish',
    '> ESC (R'       : 'designate G0 charset: French',
    '> ESC (Q'       : 'designate G0 charset: French Canadian',
    '> ESC (K'       : 'designate G0 charset: German',
    '> ESC (I'       : 'designate G0 charset: Italian',
    '> ESC (E'       : 'designate G0 charset: Norwegian/Danish',
    '> ESC (6'       : 'designate G0 charset: Norwegian/Danish',
    '> ESC (Z'       : 'designate G0 charset: Spanish',
    '> ESC (H'       : 'designate G0 charset: Swedish',
    '> ESC (7'       : 'designate G0 charset: Swedish',
    '> ESC (='       : 'designate G0 charset: Swiss',
    '> ESC )0'       : 'designate G1 charset: DEC Special Character and Line Drawing Set',
    '> ESC )A'       : 'designate G1 charset: United Kingdom (UK)',
    '> ESC )B'       : 'designate G1 charset: United States (USASCII)',
    '> ESC )4'       : 'designate G1 charset: Dutch',
    '> ESC )C'       : 'designate G1 charset: Finnish',
    '> ESC )5'       : 'designate G1 charset: Finnish',
    '> ESC )R'       : 'designate G1 charset: French',
    '> ESC )Q'       : 'designate G1 charset: French Canadian',
    '> ESC )K'       : 'designate G1 charset: German',
    '> ESC )I'       : 'designate G1 charset: Italian',
    '> ESC )E'       : 'designate G1 charset: Norwegian/Danish',
    '> ESC )6'       : 'designate G1 charset: Norwegian/Danish',
    '> ESC )Z'       : 'designate G1 charset: Spanish',
    '> ESC )H'       : 'designate G1 charset: Swedish',
    '> ESC )7'       : 'designate G1 charset: Swedish',
    '> ESC )='       : 'designate G1 charset: Swiss',
    '> ESC *0'       : 'designate G2 charset: DEC Special Character and Line Drawing Set',
    '> ESC *A'       : 'designate G2 charset: United Kingdom (UK)',
    '> ESC *B'       : 'designate G2 charset: United States (USASCII)',
    '> ESC *4'       : 'designate G2 charset: Dutch',
    '> ESC *C'       : 'designate G2 charset: Finnish',
    '> ESC *5'       : 'designate G2 charset: Finnish',
    '> ESC *R'       : 'designate G2 charset: French',
    '> ESC *Q'       : 'designate G2 charset: French Canadian',
    '> ESC *K'       : 'designate G2 charset: German',
    '> ESC *I'       : 'designate G2 charset: Italian',
    '> ESC *E'       : 'designate G2 charset: Norwegian/Danish',
    '> ESC *6'       : 'designate G2 charset: Norwegian/Danish',
    '> ESC *Z'       : 'designate G2 charset: Spanish',
    '> ESC *H'       : 'designate G2 charset: Swedish',
    '> ESC *7'       : 'designate G2 charset: Swedish',
    '> ESC *='       : 'designate G2 charset: Swiss',
    '> ESC +0'       : 'designate G3 charset: DEC Special Character and Line Drawing Set',
    '> ESC +A'       : 'designate G3 charset: United Kingdom (UK)',
    '> ESC +B'       : 'designate G3 charset: United States (USASCII)',
    '> ESC +4'       : 'designate G3 charset: Dutch',
    '> ESC +C'       : 'designate G3 charset: Finnish',
    '> ESC +5'       : 'designate G3 charset: Finnish',
    '> ESC +R'       : 'designate G3 charset: French',
    '> ESC +Q'       : 'designate G3 charset: French Canadian',
    '> ESC +K'       : 'designate G3 charset: German',
    '> ESC +I'       : 'designate G3 charset: Italian',
    '> ESC +E'       : 'designate G3 charset: Norwegian/Danish',
    '> ESC +6'       : 'designate G3 charset: Norwegian/Danish',
    '> ESC +Z'       : 'designate G3 charset: Spanish',
    '> ESC +H'       : 'designate G3 charset: Swedish',
    '> ESC +7'       : 'designate G3 charset: Swedish',
    '> ESC +='       : 'designate G3 charset: Swiss',
    '> ESC P<ST>'    : 'DCS',
    '> ESC ]<ST>'    : 'OSC',
    '> ESC ^<ST>'    : 'PM',
    '> ESC _<ST>'    : 'APC',
    '> ESC X<ST>'    : 'SOS',
    '> CSI @'        : 'ICH / insert blank characters',
    '> CSI [0]@'     : 'ICH 1 / insert a blank character',
    '> CSI A'        : 'CUU / cursor up',
    '> CSI [0]A'     : 'CUU 1 / cursor up',
    '> CSI B'        : 'CUD / cursor down',
    '> CSI [0]B'     : 'CUD 1 / cursor down',
    '> CSI C'        : 'CUF / cursor forward',
    '> CSI [0]C'     : 'CUF 1 / cursor forward',
    '> CSI D'        : 'CUB / cursor backward',
    '> CSI [0]D'     : 'CUB 1 / cursor backward',
    '> CSI E'        : 'CNL / cursor next line',
    '> CSI [0]E'     : 'CNL 1 / cursor next line',
    '> CSI F'        : 'CPL / cursor preceding line',
    '> CSI [0]F'     : 'CPL 1 / cursor preceding line',
    '> CSI G'        : 'CHA / cursor character absolute',
    '> CSI [0]G'     : 'CHA 1 / cursor character absolute',
    '> CSI H'        : 'CUP',
    '> CSI [2]H'     : 'CUP / move cursor to (row, col)',
    '> CSI [0]H'     : 'CUP / move cursor to (1, 1)',
    '> CSI I'        : 'CHT / cursor forward tabulation',
    '> CSI [0]I'     : 'CHT 1 / cursor forward tabulation',
    '> CSI J'        : 'ED / erase display',
    '> CSI [0]J'     : 'ED 0 / erase display: from cursor through the end of the display',
    '> CSI 0J'       : 'ED 0 / erase display: from cursor through the end of the display',
    '> CSI 1J'       : 'ED 1 / erase display: from the beginning of the display through the cursor',
    '> CSI 2J'       : 'ED 2 / erase display: the complete of display',
    '> CSI K'        : 'EL / erase line',
    '> CSI [0]K'     : 'EL 0 / erase line: from the cursor through the end of the line',
    '> CSI 0K'       : 'EL 0 / erase line: from the cursor through the end of the line',
    '> CSI 1K'       : 'EL 1 / erase line: from the beginning of the line through the cursor',
    '> CSI 2K'       : 'EL 2 / erase line: the complete of line',
    '> CSI L'        : 'IL / insert lines',
    '> CSI [0]L'     : 'IL 1 / insert a line',
    '> CSI M'        : 'DL / delete lines',
    '> CSI [0]M'     : 'DL 1 / delete a line',
    '> CSI P'        : 'DCH / delete characters',
    '> CSI [0]P'     : 'DCH 1 / delete a character',
    '> CSI S'        : 'SU / scroll up',
    '> CSI [0]S'     : 'SU 1 / scroll up',
    '> CSI T'        : 'SD / scroll down',
    '> CSI T'        : 'SD 1 / scroll down',
    '> CSI [1]T'     : 'SD / scroll down',
    '> CSI [5]T'     : 'Initiate Highlight Mouse Tracking (xterm)',
    '> CSI >T'       : 'Title Mode Setting (xterm)',
    '> CSI >0T'      : 'Title Mode Setting (xterm) 0: Do not set window/icon labels using hexadecimal',
    '> CSI >1T'      : 'Title Mode Setting (xterm) 1: Do not query window/icon labels using hexadecimal',
    '> CSI >2T'      : 'Title Mode Setting (xterm) 2: Do not set window/icon labels using UTF-8',
    '> CSI >3T'      : 'Title Mode Setting (xterm) 3: Do not query window/icon labels using UTF-8',
    '> CSI X'        : 'ECH / erase characters',
    '> CSI [0]X'     : 'ECH 1 / erase a character',
    '> CSI Z'        : 'CBT / cursor backward tabulation',
    '> CSI [0]Z'     : 'CBT 1 / cursor backward tabulation',
    '> CSI `'        : 'HPA / horizontal position absolute',
    '> CSI [0]`'     : 'HPA 1 / horizontal position absolute',
    '> CSI a'        : 'HPR / horizontal position relative',
    '> CSI [0]a'     : 'HPR 1 / horizontal position relative',
    '> CSI b'        : 'REP / repeat',
    '> CSI c'        : 'DA1 / request primary device attribute',
    '> CSI > c'      : 'DA2 / request secondary device attribute',
    '> CSI d'        : 'VPA / vertical position absolute',
    '> CSI e'        : 'VPR / vertical position relative',
    '> CSI f'        : 'HVP / horizontal and vertical position',
    '> CSI g'        : 'TBC / tab clear',
    '> CSI h'        : 'SM / set mode',
    '> CSI ?h'       : 'DECSET',
    '> CSI ?1h'      : 'DECSET 1 - DECCKM / application cursor keys',
    '> CSI ?2h'      : 'DECSET 2 - DECANM / designate USASCII for character sets G0-G3 (DECANM), and set VT100 mode',
    '> CSI ?3h'      : 'DECSET 3 - DECCOLM / 132 column mode',
    '> CSI ?4h'      : 'DECSET 4 - DECSCLM / enable smooth scroll mode',
    '> CSI ?5h'      : 'DECSET 5 - DECSCNM / enable reverse video',
    '> CSI ?6h'      : 'DECSET 6 - DECOM / enable origin mode',
    '> CSI ?7h'      : 'DECSET 7 - DECAWM / enable auto-wrap mode',
    '> CSI ?8h'      : 'DECSET 8 - DECARM / disable auto repeat keys',
    '> CSI ?9h'      : 'DECSET 9 / enable X10 compatible mouse mode',
    '> CSI ?10h'     : 'DECSET 10 / show toolbar (rxvt)',
    '> CSI ?12h'     : 'DECSET 12 / blinking cursor (att610)',
    '> CSI ?25h'     : 'DECSET 25 - DECTCEM / show cursor',
    '> CSI ?1000h'   : 'DECSET 1000 / enable xterm normal mouse tracking',
    '> CSI ?1001h'   : 'DECSET 1001 / enable highlight mouse tracking',
    '> CSI ?1002h'   : 'DECSET 1002 / enable button mouse tracking',
    '> CSI ?1003h'   : 'DECSET 1003 / enable all mouse tracking',
    '> CSI ?1004h'   : 'DECSET 1004 / enable focus tracking',
    '> CSI ?1005h'   : 'DECSET 1005 / enable UTF8 mouse mode',
    '> CSI ?1006h'   : 'DECSET 1006 / enable SGR mouse mode',
    '> CSI ?1007h'   : 'DECSET 1007 / enable alternate scroll mode',
    '> CSI ?2004h'   : 'DECSET 2004 / enable bracketed paste mode',
    '> CSI i'        : 'MC',
    '> CSI ?i'       : 'MC - DEC Specific',
    '> CSI l'        : 'RM',
    '> CSI ?l'       : 'DECRST',
    '> CSI ?1l'      : 'DECRST 1 - DECCKM / normal cursor keys',
    '> CSI ?2l'      : 'DECRST 2 - DECANM / VT52 mode',
    '> CSI ?3l'      : 'DECRST 3 - DECCOLM / 80 column mode',
    '> CSI ?4l'      : 'DECRST 4 - DECSCLM / disable smooth scroll mode',
    '> CSI ?5l'      : 'DECRST 5 - DECSCNM / disable reverse video',
    '> CSI ?6l'      : 'DECRST 6 - DECOM / disable origin mode',
    '> CSI ?7l'      : 'DECRST 7 - DECAWM / disable auto-wrap mode',
    '> CSI ?8l'      : 'DECRST 8 - DECARM / disable auto repeat keys',
    '> CSI ?9l'      : 'DECRST 9 / disable X10 compatible mouse mode',
    '> CSI ?10l'     : 'DECRST 10 / hide toolbar (rxvt)',
    '> CSI ?12l'     : 'DECRST 12 / steady cursor',
    '> CSI ?25l'     : 'DECRST 25 - DECTCEM / hide cursor',
    '> CSI ?1000l'   : 'DECRST 1000 / disable xterm normal mouse mode',
    '> CSI ?1001l'   : 'DECRST 1001 / disable highlight mouse tracking',
    '> CSI ?1002l'   : 'DECRST 1002 / disable button mouse tracking',
    '> CSI ?1003l'   : 'DECRST 1003 / disable all mouse tracking',
    '> CSI ?1004l'   : 'DECRST 1004 / disable focus tracking',
    '> CSI ?1005l'   : 'DECRST 1005 / disable UTF8 mouse mode',
    '> CSI ?1006l'   : 'DECRST 1006 / disable SGR mouse mode',
    '> CSI ?1007l'   : 'DECRST 1007 / disable alternate scroll mode',
    '> CSI ?2004l'   : 'DECRST 2004 / reset bracketed paste mode',
    '> CSI m'        : 'SGR',
    '> CSI 0m'       : 'SGR 0 / reset',
    '> CSI [0]m'     : 'SGR 0 / reset',
    '> CSI 1m'       : 'SGR 1 / bold',
    '> CSI 4m'       : 'SGR 4 / underlined',
    '> CSI 5m'       : 'SGR 5 / blink',
    '> CSI 7m'       : 'SGR 7 / inverse',
    '> CSI 22m'      : 'SGR 22 / normal (neigher bold nor faint)',
    '> CSI 25m'      : 'SGR 25 / steady (not blinking)',
    '> CSI 27m'      : 'SGR 27 / positive (not inverse)',
    '> CSI 30m'      : 'SGR 30 / set fourground color to black',
    '> CSI 31m'      : 'SGR 31 / set fourground color to red',
    '> CSI 32m'      : 'SGR 32 / set fourground color to green',
    '> CSI 33m'      : 'SGR 33 / set fourground color to yellow',
    '> CSI 34m'      : 'SGR 34 / set fourground color to blue',
    '> CSI 35m'      : 'SGR 35 / set fourground color to magenta',
    '> CSI 36m'      : 'SGR 36 / set fourground color to cyan',
    '> CSI 37m'      : 'SGR 37 / set fourground color to white',
    '> CSI 39m'      : 'SGR 39 / set fourground color to default',
    '> CSI 40m'      : 'SGR 40 / set background color to black',
    '> CSI 41m'      : 'SGR 41 / set background color to red',
    '> CSI 42m'      : 'SGR 42 / set background color to green',
    '> CSI 43m'      : 'SGR 43 / set background color to yellow',
    '> CSI 44m'      : 'SGR 44 / set background color to blue',
    '> CSI 45m'      : 'SGR 45 / set background color to magenta',
    '> CSI 46m'      : 'SGR 46 / set background color to cyan',
    '> CSI 47m'      : 'SGR 47 / set background color to white',
    '> CSI 49m'      : 'SGR 49 / set background color to default',
    '> CSI 90m'      : 'SGR 90 / set foreground color to gray',
    '> CSI 91m'      : 'SGR 91 / set foreground color to bright red',
    '> CSI 92m'      : 'SGR 92 / set foreground color to bright green',
    '> CSI 93m'      : 'SGR 93 / set foreground color to bright yellow',
    '> CSI 94m'      : 'SGR 94 / set foreground color to bright blue',
    '> CSI 95m'      : 'SGR 95 / set foreground color to bright magenta',
    '> CSI 96m'      : 'SGR 96 / set foreground color to bright cyan',
    '> CSI 97m'      : 'SGR 97 / set foreground color to bright white',
    '> CSI 100m'     : 'SGR 100 / set background color to gray',
    '> CSI 101m'     : 'SGR 101 / set background color to bright red',
    '> CSI 102m'     : 'SGR 102 / set background color to bright green',
    '> CSI 103m'     : 'SGR 103 / set background color to bright yellow',
    '> CSI 104m'     : 'SGR 104 / set background color to bright blue',
    '> CSI 105m'     : 'SGR 105 / set background color to bright magenta',
    '> CSI 106m'     : 'SGR 106 / set background color to bright cyan',
    '> CSI 107m'     : 'SGR 107 / set background color to bright white',
    '> CSI >m'       : 'Special Keyboard Modifier Settings (xterm)',
    '> CSI n'        : 'DSR / request device status report',
    '> CSI 5n'       : 'DSR - OS 5 / request operating status',
    '> CSI 6n'       : 'DSR - CPR / request cursor position report',
    '> CSI ?n'       : 'DSR - DEC Specific',
    '> CSI ?6n'      : 'DSR - DECXCPR / requests cursor position report, DEC Specific',
    '> CSI >n'       : 'Disable Special Keyboard Modifier Settings (xterm)',
    '> CSI r'        : 'DECSTBM',
    '> CSI t'        : 'DECSLPP or Window Manipulation (dtterm)'
}

def get():
    return _SEQDB

