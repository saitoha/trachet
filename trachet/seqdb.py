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

'''
Reference:

- Xterm Control Sequences
  http://invisible-island.net/xterm/ctlseqs/ctlseqs.html

- TeraTerm / Supported Control Functions
  http://ttssh2.sourceforge.jp/manual/en/about/ctrlseq.html

'''

_SEQDB = {
    '< <BEL>'            : 'BEL / Ctrl-G',
    '> <BEL>'            : 'BEL / bell',
    '> ESC P<ST>'        : 'DCS / device control string',
    '> ESC ]<ST>'        : 'OSC / operating system command',
    '> ESC ]0<ST>'       : 'OSC 0 / set icon name and window title',
    '> ESC ]1<ST>'       : 'OSC 1 / set icon name',
    '> ESC ]2<ST>'       : 'OSC 2 / set window title',
    '> ESC ]4<ST>'       : 'OSC 4 / get or set color palette',
    '> ESC ]9<ST>'       : 'OSC 9 / Growl integration (iTerm2)',
    '> ESC ]10<ST>'      : 'OSC 10 / get or set foreground color',
    '> ESC ]11<ST>'      : 'OSC 11 / get or set background color',
    '> ESC ]12<ST>'      : 'OSC 12 / get or set cursor color',
    '> ESC ]13<ST>'      : 'OSC 13 / get or set mouse foreground color',
    '> ESC ]14<ST>'      : 'OSC 13 / get or set mouse background color',
    '> ESC ]51<ST>'      : 'OSC 51 / reserved for Emacs',
    '> ESC ]52<ST>'      : 'OSC 52 - PASTE64 / base64 clipboard read/write operation (xterm)',
    '> ESC ^<ST>'        : 'PM / private message',
    '> ESC _<ST>'        : 'APC / application program command',
    '> ESC V'            : 'SPA / start of guarded area',
    '> ESC W'            : 'EPA / end of guarded area',
    '> ESC X<ST>'        : 'SOS / start of string',
    '< CSI [0]M'         : 'xterm normal mouse reporting, following 3 bytes mean (code, row, col)',
    '< CSI M'            : 'URXVT (1015) mouse reporting (code,row,col)',
    '< CSI [3]M'         : 'URXVT (1015) mouse reporting (code=(%s-32),row=%s,col=%s)',
    '< CSI <[3]M'        : 'SGR (1006) mouse reporting (code=%s,row=%s,col=%s)',
    '< CSI <M'           : 'SGR (1006) mouse reporting (code,row,col)',
    '< CSI <[3]m'        : 'SGR (1006) mouse reporting, button up (code=%s,row=%s,col=%s)',
    '< CSI <m'           : 'SGR (1006) mouse reporting, button up (code, row, col)',
    '< CSI [3]R'         : 'DSR-DECXCPR(cursor position report) response, DEC specific: (row=%s,col=%s,page=%s)',
    '< CSI [2]R'         : 'DSR-CPR(cursor position report) response: (row=%s,col=%s)',
    '< CSI R'            : 'DSR-CPR(cursor position report) response',
    '< CSI 0n'           : 'DSR-OS(operating status report) response: "good status"',
    '< CSI 3n'           : 'DSR-OS(operating status report) response: "it has a malfunction"',
    '< CSI ?c'           : 'DA1 Response',
    '< CSI ?1;2c'        : 'DA1 Response: VT100 with AVO (could be a VT102/rxvt/rxvt-unicode/konsole/kterm/mlterm/iTerm2/tmux/aterm/wterm/Terminal.app(Mac)/mrxvt/MinTTY/TeraTerm/ck)',
    '< CSI ?1;0c'        : 'DA1 Response: VT100 with no options',
    '< CSI ?6c'          : 'DA1 Response: VT102 (could be linux xvt/console/PuTTY/Terminal.app(GNUStep)/yaft)',
    '< CSI ?62c'         : 'DA1 Response: VT200 family (could be mosh)',
    '< CSI ?62;9;c'      : 'DA1 Response: VT200 family (could be gnome-terminal)',
    '< CSI ?64;1;2;6;9;15;21;22c':
    'DA1 Response: VT400 family (could be xterm pl>=280)',
    '< CSI ?65;1;2;3,4;6;8;9;18;21;22;29;42;44c':
    'DA1 Response: VT500 family (could be RLogin)',
    '< CSI >c'           : 'DA2 Response',
    '< CSI >0;[*]c'      : 'DA2 Response: VT100',
    '< CSI >0;95;c'      : 'DA2 Response: xterm pattch#95 (could be iTerm/iTerm2)',
    '< CSI >0;95;0c'     : 'DA2 Response: xterm pattch#95 (could be tmux/)',
    '< CSI >0;95;1c'     : 'DA2 Response: xterm pattch#95 (could be avaliable mouse)',
    '< CSI >0;115;0c'    : 'DA2 Response: xterm pattch#115 (could be Konsole)',
    '< CSI >0;136;0c'    : 'DA2 Response: xterm pattch#136 (could be PuTTY)',
    '< CSI >0;270;0c'    : 'DA2 Response: VT100 (could be xterm patch#270)',
    '< CSI >0;271;0c'    : 'DA2 Response: VT100 (could be xterm patch#271)',
    '< CSI >0;272;0c'    : 'DA2 Response: VT100 (could be xterm patch#272)',
    '< CSI >0;273;0c'    : 'DA2 Response: VT100 (could be xterm patch#273)',
    '< CSI >0;274;0c'    : 'DA2 Response: VT100 (could be xterm patch#274)',
    '< CSI >0;275;0c'    : 'DA2 Response: VT100 (could be xterm patch#275)',
    '< CSI >0;276;0c'    : 'DA2 Response: VT100 (could be xterm patch#276)',
    '< CSI >0;277;0c'    : 'DA2 Response: VT100 (could be xterm patch#277)',
    '< CSI >0;278;0c'    : 'DA2 Response: VT100 (could be xterm patch#278)',
    '< CSI >0;279;0c'    : 'DA2 Response: VT100 (could be xterm patch#279)',
    '< CSI >1;[*]c'      : 'DA2 Response: VT220',
    '< CSI >1;10;0c'     : 'DA2 Response: VT220 (could be mosh)',
    '< CSI >1;96;0c'     : 'DA2 Response: VT220 (could be xterm pattch#96, mlterm)',
    '< CSI >1;2403;0c'   : 'DA2 Response: VT220 (could be VTE, such as gnome-terminal)',
    '< CSI >1;2802;0c'   : 'DA2 Response: VT220 (could be VTE, such as gnome-terminal)',
    '< CSI >2;[2]c'      : 'DA2 Response: VT240',
    '< CSI >18;[2]c'     : 'DA2 Response: VT330',
    '< CSI >19;[2]c'     : 'DA2 Response: VT340',
    '< CSI >19;[2]c'     : 'DA2 Response: VT340',
    '< CSI >24;[2]c'     : 'DA2 Response: VT320',
    '< CSI >32;[2]c'     : 'DA2 Response: VT382',
    '< CSI >32;100;2c'   : 'DA2 Response: VT382 (could be TeraTerm)',
    '< CSI >41;[2]c'     : 'DA2 Response: VT420',
    '< CSI >41;280;0c'   : 'DA2 Response: VT420 (could be xterm patch#280)',
    '< CSI >41;281;0c'   : 'DA2 Response: VT420 (could be xterm patch#281)',
    '< CSI >41;282;0c'   : 'DA2 Response: VT420 (could be xterm patch#282)',
    '< CSI >41;283;0c'   : 'DA2 Response: VT420 (could be xterm patch#283)',
    '< CSI >41;284;0c'   : 'DA2 Response: VT420 (could be xterm patch#284)',
    '< CSI >41;285;0c'   : 'DA2 Response: VT420 (could be xterm patch#285)',
    '< CSI >41;286;0c'   : 'DA2 Response: VT420 (could be xterm patch#286)',
    '< CSI >41;287;0c'   : 'DA2 Response: VT420 (could be xterm patch#287)',
    '< CSI >41;288;0c'   : 'DA2 Response: VT420 (could be xterm patch#288)',
    '< CSI >41;289;0c'   : 'DA2 Response: VT420 (could be xterm patch#289)',
    '< CSI >41;290;0c'   : 'DA2 Response: VT420 (could be xterm patch#290)',
    '< CSI >41;291;0c'   : 'DA2 Response: VT420 (could be xterm patch#291)',
    '< CSI >41;292;0c'   : 'DA2 Response: VT420 (could be xterm patch#292)',
    '< CSI >61;[2]c'     : 'DA2 Response: VT510',
    '< CSI >64;[2]c'     : 'DA2 Response: VT520',
    '< CSI >65;[2]c'     : 'DA2 Response: VT525',
    '< CSI >65;100;1c'   : 'DA1 Response: VT500 family (could be RLogin)',
    '< CSI >77;[2]c'     : 'DA2 Response: could be MinTTY',
    '< CSI >77;10003;c'  : 'DA2 Response: could be MinTTY 1.0.3',
    '< CSI >82;[*]c'     : 'DA2 Response: could be mrxvt',
    '< CSI >82;20710;0c' : 'DA2 Response: could be rxvt/ck',
    '< CSI >82;0.5.4;0c' : 'DA2 Response: could be mrxvt 0.5.4',
    '< CSI >83;[*]c'     : 'DA2 Response: could be GNU Screen',
    '< CSI >83;40000;0c' : 'DA2 Response: could be GNU Screen 4.0.0',
    '< CSI >83;40001;0c' : 'DA2 Response: could be GNU Screen 4.0.1',
    '< CSI >83;40002;0c' : 'DA2 Response: could be GNU Screen 4.0.2',
    '< CSI >83;40003;0c' : 'DA2 Response: could be GNU Screen 4.0.3',
    '< CSI >83;40100;0c' : 'DA2 Response: could be GNU Screen 4.1.0',
    '< CSI >85;95;c'     : 'DA2 Response: could be rxvt-unicode',
    '< CSI 15~'          : 'F5 key (xterm)',
    '< CSI 17~'          : 'F6 key (xterm)',
    '< CSI 18~'          : 'F7 key (xterm)',
    '< CSI 19~'          : 'F8 key (xterm)',
    '< CSI 20~'          : 'F9 key (xterm)',
    '< CSI 21~'          : 'F10 key (xterm)',
    '< CSI 23~'          : 'F11 key (xterm)',
    '< CSI 24~'          : 'F12 key (xterm)',
    '> ESC D'            : 'IND / moves the cursor down one line in the same column',
    '> ESC E'            : 'NEL / moves the cursor to the first position on the next line',
    '> ESC H'            : 'HTS / sets a horizontal tab stop at the column where the cursor is. ',
    '> ESC M'            : 'HTS / moves the cursor up one line in the same column',
    '> ESC N'            : 'SS2 / temporarily maps the G2 character set into GL or GR, for the next graphic character',
    '> ESC O'            : 'SS3 / temporarily maps the G3 character set into GL or GR, for the next graphic character',
    '> ESC \\'           : 'ST / String terminator. Ends a DCS, SOS, OSC, PM and APC sequence',
    '> ESC 6'            : 'DECBI / backward index',
    '> ESC 7'            : 'DECSC / save cursor',
    '> ESC 8'            : 'DECRC / restore cursor',
    '> ESC 9'            : 'DECFI / forward index',
    '> ESC ='            : 'DECKPAM / application keypad',
    '> ESC >'            : 'DECKPNM / normal keypad',
    '> ESC c'            : 'RIS / full reset',
    '> ESC <SP>F'        : 'S7C1T',
    '> ESC <SP>G'        : 'S8C1T',
    '> ESC <SP>L'        : 'Set ANSI conformance level 1',
    '> ESC <SP>M'        : 'Set ANSI conformance level 2',
    '> ESC <SP>N'        : 'Set ANSI conformance level 3',
    '> ESC #3'           : 'DECDHLT / double height line, top half',
    '> ESC #4'           : 'DECDHLB / double height line, bottom half',
    '> ESC #5'           : 'DECSWL / single width line',
    '> ESC #6'           : 'DECDWL / double width line',
    '> ESC #8'           : 'DECALN / screen alignment pattern',
    '> ESC %@'           : 'Select default character set',
    '> ESC %G'           : 'Select UTF-8 character set',
    '> ESC (0'           : 'designate G0 charset: DEC Special Character and Line Drawing Set',
    '> ESC (A'           : 'designate G0 charset: United Kingdom (UK)',
    '> ESC (B'           : 'designate G0 charset: United States (USASCII)',
    '> ESC (4'           : 'designate G0 charset: Dutch',
    '> ESC (C'           : 'designate G0 charset: Finnish',
    '> ESC (5'           : 'designate G0 charset: Finnish',
    '> ESC (R'           : 'designate G0 charset: French',
    '> ESC (Q'           : 'designate G0 charset: French Canadian',
    '> ESC (K'           : 'designate G0 charset: German',
    '> ESC (I'           : 'designate G0 charset: Italian',
    '> ESC (E'           : 'designate G0 charset: Norwegian/Danish',
    '> ESC (6'           : 'designate G0 charset: Norwegian/Danish',
    '> ESC (Z'           : 'designate G0 charset: Spanish',
    '> ESC (H'           : 'designate G0 charset: Swedish',
    '> ESC (7'           : 'designate G0 charset: Swedish',
    '> ESC (='           : 'designate G0 charset: Swiss',
    '> ESC )0'           : 'designate G1 charset: DEC Special Character and Line Drawing Set',
    '> ESC )A'           : 'designate G1 charset: United Kingdom (UK)',
    '> ESC )B'           : 'designate G1 charset: United States (USASCII)',
    '> ESC )4'           : 'designate G1 charset: Dutch',
    '> ESC )C'           : 'designate G1 charset: Finnish',
    '> ESC )5'           : 'designate G1 charset: Finnish',
    '> ESC )R'           : 'designate G1 charset: French',
    '> ESC )Q'           : 'designate G1 charset: French Canadian',
    '> ESC )K'           : 'designate G1 charset: German',
    '> ESC )I'           : 'designate G1 charset: Italian',
    '> ESC )E'           : 'designate G1 charset: Norwegian/Danish',
    '> ESC )6'           : 'designate G1 charset: Norwegian/Danish',
    '> ESC )Z'           : 'designate G1 charset: Spanish',
    '> ESC )H'           : 'designate G1 charset: Swedish',
    '> ESC )7'           : 'designate G1 charset: Swedish',
    '> ESC )='           : 'designate G1 charset: Swiss',
    '> ESC *0'           : 'designate G2 charset: DEC Special Character and Line Drawing Set',
    '> ESC *A'           : 'designate G2 charset: United Kingdom (UK)',
    '> ESC *B'           : 'designate G2 charset: United States (USASCII)',
    '> ESC *4'           : 'designate G2 charset: Dutch',
    '> ESC *C'           : 'designate G2 charset: Finnish',
    '> ESC *5'           : 'designate G2 charset: Finnish',
    '> ESC *R'           : 'designate G2 charset: French',
    '> ESC *Q'           : 'designate G2 charset: French Canadian',
    '> ESC *K'           : 'designate G2 charset: German',
    '> ESC *I'           : 'designate G2 charset: Italian',
    '> ESC *E'           : 'designate G2 charset: Norwegian/Danish',
    '> ESC *6'           : 'designate G2 charset: Norwegian/Danish',
    '> ESC *Z'           : 'designate G2 charset: Spanish',
    '> ESC *H'           : 'designate G2 charset: Swedish',
    '> ESC *7'           : 'designate G2 charset: Swedish',
    '> ESC *='           : 'designate G2 charset: Swiss',
    '> ESC +0'           : 'designate G3 charset: DEC Special Character and Line Drawing Set',
    '> ESC +A'           : 'designate G3 charset: United Kingdom (UK)',
    '> ESC +B'           : 'designate G3 charset: United States (USASCII)',
    '> ESC +4'           : 'designate G3 charset: Dutch',
    '> ESC +C'           : 'designate G3 charset: Finnish',
    '> ESC +5'           : 'designate G3 charset: Finnish',
    '> ESC +R'           : 'designate G3 charset: French',
    '> ESC +Q'           : 'designate G3 charset: French Canadian',
    '> ESC +K'           : 'designate G3 charset: German',
    '> ESC +I'           : 'designate G3 charset: Italian',
    '> ESC +E'           : 'designate G3 charset: Norwegian/Danish',
    '> ESC +6'           : 'designate G3 charset: Norwegian/Danish',
    '> ESC +Z'           : 'designate G3 charset: Spanish',
    '> ESC +H'           : 'designate G3 charset: Swedish',
    '> ESC +7'           : 'designate G3 charset: Swedish',
    '> ESC +='           : 'designate G3 charset: Swiss',
    '> ESC P<ST>'        : 'DCS',
    '> ESC ]<ST>'        : 'OSC',
    '> ESC ^<ST>'        : 'PM',
    '> ESC _<ST>'        : 'APC',
    '> ESC X<ST>'        : 'SOS',
    '> CSI @'            : 'ICH / insert blank characters',
    '> CSI [0]@'         : 'ICH 1 / insert a blank character',
    '> CSI A'            : 'CUU / cursor up',
    '> CSI [0]A'         : 'CUU 1 / cursor up',
    '> CSI B'            : 'CUD / cursor down',
    '> CSI [0]B'         : 'CUD 1 / cursor down',
    '> CSI C'            : 'CUF / cursor forward',
    '> CSI [0]C'         : 'CUF 1 / cursor forward',
    '> CSI D'            : 'CUB / cursor backward',
    '> CSI [0]D'         : 'CUB 1 / cursor backward',
    '> CSI E'            : 'CNL / cursor next line',
    '> CSI [0]E'         : 'CNL 1 / cursor next line',
    '> CSI F'            : 'CPL / cursor preceding line',
    '> CSI [0]F'         : 'CPL 1 / cursor preceding line',
    '> CSI G'            : 'CHA / cursor character absolute',
    '> CSI [0]G'         : 'CHA 1 / cursor character absolute',
    '> CSI H'            : 'CUP',
    '> CSI [2]H'         : 'CUP / move cursor to (row=%s, col=%s)',
    '> CSI [0]H'         : 'CUP / move cursor to (1, 1)',
    '> CSI I'            : 'CHT / cursor forward tabulation',
    '> CSI [0]I'         : 'CHT 1 / cursor forward tabulation',
    '> CSI J'            : 'ED / erase display',
    '> CSI [0]J'         : 'ED 0 / erase display: from cursor through the end of the display',
    '> CSI 0J'           : 'ED 0 / erase display: from cursor through the end of the display',
    '> CSI 1J'           : 'ED 1 / erase display: from the beginning of the display through the cursor',
    '> CSI 2J'           : 'ED 2 / erase display: the complete of display',
    '> CSI K'            : 'EL / erase line',
    '> CSI [0]K'         : 'EL 0 / erase line: from the cursor through the end of the line',
    '> CSI 0K'           : 'EL 0 / erase line: from the cursor through the end of the line',
    '> CSI 1K'           : 'EL 1 / erase line: from the beginning of the line through the cursor',
    '> CSI 2K'           : 'EL 2 / erase line: the complete of line',
    '> CSI L'            : 'IL / insert lines',
    '> CSI [0]L'         : 'IL 1 / insert a line',
    '> CSI M'            : 'DL / delete lines',
    '> CSI [0]M'         : 'DL 1 / delete a line',
    '> CSI P'            : 'DCH / delete characters',
    '> CSI [0]P'         : 'DCH 1 / delete a character',
    '> CSI S'            : 'SU / scroll up',
    '> CSI [0]S'         : 'SU 1 / scroll up',
    '> CSI T'            : 'SD / scroll down',
    '> CSI T'            : 'SD 1 / scroll down',
    '> CSI [1]T'         : 'SD / scroll down %s times',
    '> CSI [6]T'         : 'Initiate highlight mouse tracking (startx=%s,starty=%s,endx=%s,endy=%s,mousex=%s,mousey=%s)',
    '> CSI >T'           : 'Title Mode Setting (xterm)',
    '> CSI >0T'          : 'Title Mode Setting (xterm) 0: Do not set window/icon labels using hexadecimal',
    '> CSI >1T'          : 'Title Mode Setting (xterm) 1: Do not query window/icon labels using hexadecimal',
    '> CSI >2T'          : 'Title Mode Setting (xterm) 2: Do not set window/icon labels using UTF-8',
    '> CSI >3T'          : 'Title Mode Setting (xterm) 3: Do not query window/icon labels using UTF-8',
    '> CSI X'            : 'ECH / erase characters',
    '> CSI [0]X'         : 'ECH 1 / erase a character',
    '> CSI Z'            : 'CBT / cursor backward tabulation',
    '> CSI [0]Z'         : 'CBT 1 / cursor backward tabulation',
    '> CSI `'            : 'HPA / horizontal position absolute',
    '> CSI [0]`'         : 'HPA 1 / horizontal position absolute',
    '> CSI a'            : 'HPR / horizontal position relative',
    '> CSI [0]a'         : 'HPR 1 / horizontal position relative',
    '> CSI b'            : 'REP / repeat',
    '> CSI c'            : 'DA1 / request primary device attribute',
    '> CSI >c'           : 'DA2 / request secondary device attribute',
    '> CSI d'            : 'VPA / vertical position absolute',
    '> CSI e'            : 'VPR / vertical position relative',
    '> CSI f'            : 'HVP / horizontal and vertical position',
    '> CSI g'            : 'TBC / tab clear',
    '> CSI h'            : 'SM / set mode',
    '> CSI ?h'           : 'DECSET',
    '> CSI ?1h'          : 'DECSET 1 - DECCKM / application cursor keys',
    '> CSI ?2h'          : 'DECSET 2 - DECANM / designate USASCII for G0-G3 (DECANM), and set VT100 mode',
    '> CSI ?3h'          : 'DECSET 3 - DECCOLM / 132 column mode',
    '> CSI ?4h'          : 'DECSET 4 - DECSCLM / enable smooth scroll mode',
    '> CSI ?5h'          : 'DECSET 5 - DECSCNM / enable reverse video',
    '> CSI ?6h'          : 'DECSET 6 - DECOM / enable origin mode',
    '> CSI ?7h'          : 'DECSET 7 - DECAWM / enable auto-wrap mode',
    '> CSI ?8h'          : 'DECSET 8 - DECARM / disable auto repeat keys',
    '> CSI ?9h'          : 'DECSET 9 / enable X10 compatible mouse mode',
    '> CSI ?10h'         : 'DECSET 10 / show toolbar (rxvt)',
    '> CSI ?12h'         : 'DECSET 12 / blinking cursor (att610)',
    '> CSI ?12;25h'      : 'DECSET 12;25 / visible and blinking cursor',
    '> CSI ?25h'         : 'DECSET 25 - DECTCEM / show cursor',
    '> CSI ?1000h'       : 'DECSET 1000 / enable xterm normal mouse tracking',
    '> CSI ?1001h'       : 'DECSET 1001 / enable highlight mouse tracking',
    '> CSI ?1002h'       : 'DECSET 1002 / enable button mouse tracking',
    '> CSI ?1003h'       : 'DECSET 1003 / enable all mouse tracking',
    '> CSI ?1004h'       : 'DECSET 1004 / enable focus tracking',
    '> CSI ?1005h'       : 'DECSET 1005 / enable UTF8 mouse mode',
    '> CSI ?1006h'       : 'DECSET 1006 / enable SGR mouse mode',
    '> CSI ?1007h'       : 'DECSET 1007 / enable alternate scroll mode',
    '> CSI ?1047h'       : 'DECSET 1047 / use alternate screen buffer',
    '> CSI ?1049h'       : 'DECSET 1049 / save cursor as in DECSC and use alternate screen buffer',
    '> CSI ?2004h'       : 'DECSET 2004 / enable bracketed paste mode',
    '> CSI ?7700h'       : 'DECSET 7700 / enable ambiguous reporting (mintty)',
    '> CSI i'            : 'MC',
    '> CSI ?i'           : 'MC - DEC Specific',
    '> CSI l'            : 'RM',
    '> CSI ?l'           : 'DECRST',
    '> CSI ?1l'          : 'DECRST 1 - DECCKM / normal cursor keys',
    '> CSI ?2l'          : 'DECRST 2 - DECANM / VT52 mode',
    '> CSI ?3l'          : 'DECRST 3 - DECCOLM / 80 column mode',
    '> CSI ?4l'          : 'DECRST 4 - DECSCLM / disable smooth scroll mode',
    '> CSI ?5l'          : 'DECRST 5 - DECSCNM / disable reverse video',
    '> CSI ?6l'          : 'DECRST 6 - DECOM / disable origin mode',
    '> CSI ?7l'          : 'DECRST 7 - DECAWM / disable auto-wrap mode',
    '> CSI ?8l'          : 'DECRST 8 - DECARM / disable auto repeat keys',
    '> CSI ?9l'          : 'DECRST 9 / disable X10 compatible mouse mode',
    '> CSI ?10l'         : 'DECRST 10 / hide toolbar (rxvt)',
    '> CSI ?12l'         : 'DECRST 12 / steady cursor',
    '> CSI ?25l'         : 'DECRST 25 - DECTCEM / hide cursor',
    '> CSI ?1000l'       : 'DECRST 1000 / disable xterm normal mouse mode',
    '> CSI ?1001l'       : 'DECRST 1001 / disable highlight mouse tracking',
    '> CSI ?1002l'       : 'DECRST 1002 / disable button mouse tracking',
    '> CSI ?1003l'       : 'DECRST 1003 / disable all mouse tracking',
    '> CSI ?1004l'       : 'DECRST 1004 / disable focus tracking',
    '> CSI ?1005l'       : 'DECRST 1005 / disable UTF8 mouse mode',
    '> CSI ?1006l'       : 'DECRST 1006 / disable SGR mouse mode',
    '> CSI ?1007l'       : 'DECRST 1007 / disable alternate scroll mode',
    '> CSI ?1047l'       : 'DECRST 1047 / use normal screen buffer',
    '> CSI ?1049l'       : 'DECRST 1049 / use normal screen buffer and restore cursor as in DECRC',
    '> CSI ?2004l'       : 'DECRST 2004 / reset bracketed paste mode',
    '> CSI ?7700l'       : 'DECRST 7700 / disable ambiguous reporting (mintty)',
    '> CSI m'            : 'SGR / select graphics rendition',
    '> CSI 0m'           : 'SGR 0 / reset',
    '> CSI 00m'          : 'SGR 0 / reset',
    '> CSI [0]m'         : 'SGR 0 / reset',
    '> CSI 1m'           : 'SGR 1 / bold',
    '> CSI 4m'           : 'SGR 4 / underlined',
    '> CSI 5m'           : 'SGR 5 / blink',
    '> CSI 7m'           : 'SGR 7 / inverse',
    '> CSI 22m'          : 'SGR 22 / normal (neigher bold nor faint)',
    '> CSI 24m'          : 'SGR 24 / not underlined',
    '> CSI 25m'          : 'SGR 25 / steady (not blinking)',
    '> CSI 27m'          : 'SGR 27 / positive (not inverse)',
    '> CSI 30m'          : 'SGR 30 / set fourground color to black',
    '> CSI 31m'          : 'SGR 31 / set fourground color to red',
    '> CSI 32m'          : 'SGR 32 / set fourground color to green',
    '> CSI 33m'          : 'SGR 33 / set fourground color to yellow',
    '> CSI 34m'          : 'SGR 34 / set fourground color to blue',
    '> CSI 35m'          : 'SGR 35 / set fourground color to magenta',
    '> CSI 36m'          : 'SGR 36 / set fourground color to cyan',
    '> CSI 37m'          : 'SGR 37 / set fourground color to white',
    '> CSI 39m'          : 'SGR 39 / set fourground color to default',
    '> CSI 38;5;[1]m'    : 'SGR 38;5;* / set fourground color to %s',
    '> CSI 39;49m'       : 'SGR 39;49 / set fourground and background color to default',
    '> CSI 40m'          : 'SGR 40 / set background color to black',
    '> CSI 41m'          : 'SGR 41 / set background color to red',
    '> CSI 42m'          : 'SGR 42 / set background color to green',
    '> CSI 43m'          : 'SGR 43 / set background color to yellow',
    '> CSI 44m'          : 'SGR 44 / set background color to blue',
    '> CSI 45m'          : 'SGR 45 / set background color to magenta',
    '> CSI 46m'          : 'SGR 46 / set background color to cyan',
    '> CSI 47m'          : 'SGR 47 / set background color to white',
    '> CSI 48;5;[1]m'    : 'SGR 48;5;* / set background color to %s',
    '> CSI 49m'          : 'SGR 49 / set background color to default',
    '> CSI 90m'          : 'SGR 90 / set foreground color to gray',
    '> CSI 91m'          : 'SGR 91 / set foreground color to bright red',
    '> CSI 92m'          : 'SGR 92 / set foreground color to bright green',
    '> CSI 93m'          : 'SGR 93 / set foreground color to bright yellow',
    '> CSI 94m'          : 'SGR 94 / set foreground color to bright blue',
    '> CSI 95m'          : 'SGR 95 / set foreground color to bright magenta',
    '> CSI 96m'          : 'SGR 96 / set foreground color to bright cyan',
    '> CSI 97m'          : 'SGR 97 / set foreground color to bright white',
    '> CSI 100m'         : 'SGR 100 / set background color to gray',
    '> CSI 101m'         : 'SGR 101 / set background color to bright red',
    '> CSI 102m'         : 'SGR 102 / set background color to bright green',
    '> CSI 103m'         : 'SGR 103 / set background color to bright yellow',
    '> CSI 104m'         : 'SGR 104 / set background color to bright blue',
    '> CSI 105m'         : 'SGR 105 / set background color to bright magenta',
    '> CSI 106m'         : 'SGR 106 / set background color to bright cyan',
    '> CSI 107m'         : 'SGR 107 / set background color to bright white',
    '> CSI >m'           : 'Special Keyboard Modifier Settings (xterm)',
    '> CSI n'            : 'DSR / request device status report',
    '> CSI 5n'           : 'DSR - OS / request operating status',
    '> CSI 6n'           : 'DSR - CPR / request cursor position report',
    '> CSI ?n'           : 'DSR - DEC Specific',
    '> CSI ?6n'          : 'DSR - DECXCPR / requests cursor position report, DEC Specific',
    '> CSI >p'           : 'Pointer Mode',
    '> CSI >[0]p'        : 'Pointer Mode 1: hide if the mouse tracking mode is not enabled',
    '> CSI >0p'          : 'Pointer Mode 0: never hide the pointer',
    '> CSI >1p'          : 'Pointer Mode 1: hide if the mouse tracking mode is not enabled',
    '> CSI >2p'          : 'Pointer Mode 2: always hide the pointer',
    '> CSI $p'           : 'DECRQM / request ANSI mode',
    '> CSI ?$p'          : 'DECRQM - DEC specific / request DEC private mode',
    '> CSI >n'           : 'disable special keyboard modifier settings (xterm)',
    '> CSI "p'           : 'DECSCL / set conformance level',
    '> CSI 61;0"p'       : 'DECSCL / set conformance level: VT100 8bit control',
    '> CSI 61;1"p'       : 'DECSCL / set conformance level: VT100 7bit control',
    '> CSI 61;2"p'       : 'DECSCL / set conformance level: VT100 8bit control',
    '> CSI 62;0"p'       : 'DECSCL / set conformance level: VT200 8bit control',
    '> CSI 62;1"p'       : 'DECSCL / set conformance level: VT200 7bit control',
    '> CSI 62;2"p'       : 'DECSCL / set conformance level: VT200 8bit control',
    '> CSI 63;0"p'       : 'DECSCL / set conformance level: VT300 8bit control',
    '> CSI 63;1"p'       : 'DECSCL / set conformance level: VT300 7bit control',
    '> CSI 63;2"p'       : 'DECSCL / set conformance level: VT300 8bit control',
    '> CSI <SP>q'        : 'DECSCUSR / set cursor style',
    '> CSI [0]<SP>q'     : 'DECSCUSR 1 / set cursor style: blinking block (default)',
    '> CSI 0<SP>q'       : 'DECSCUSR 0 / set cursor style: blinking block',
    '> CSI 1<SP>q'       : 'DECSCUSR 1 / set cursor style: blinking block (default)',
    '> CSI 2<SP>q'       : 'DECSCUSR 2 / set cursor style: steady block',
    '> CSI 3<SP>q'       : 'DECSCUSR 3 / set cursor style: blinking underline',
    '> CSI 4<SP>q'       : 'DECSCUSR 4 / set cursor style: steady underline',
    '> CSI 5<SP>q'       : 'DECSCUSR 5 / set cursor style: blinking bar',
    '> CSI 6<SP>q'       : 'DECSCUSR 6 / set cursor style: steady bar',
    '> CSI "q'           : 'DECSCA / select character protection attribute',
    '> CSI [0]"q'        : 'DECSCA 0 / select character protection attribute: DECSED and DECSEL can erase',
    '> CSI 0"q'          : 'DECSCA 0 / select character protection attribute: DECSED and DECSEL can erase',
    '> CSI 1"q'          : 'DECSCA 1 / select character protection attribute: DECSED and DECSEL cannot erase',
    '> CSI 2"q'          : 'DECSCA 2 / select character protection attribute: DECSED and DECSEL can erase',
    '> CSI r'            : 'DECSTBM / set top and bottom margins',
    '> CSI ?r'           : 'save DEC private mode values',
    '> CSI ?s'           : 'restore DEC private mode values',
    '> CSI t'            : 'DECSLPP or Window Manipulation (dtterm)',
    '> CSI 1t'           : 'Window Manipulation (dtterm) 1: de-iconify window',
    '> CSI 2t'           : 'Window Manipulation (dtterm) 2: iconify window',
    '> CSI 3;[2]t'       : 'Window Manipulation (dtterm) 3: move window (%s, %s)',
    '> CSI 4;[2]t'       : 'Window Manipulation (dtterm) 4: resize window in pixels (%s, %s)'
}

def get():
    return _SEQDB

