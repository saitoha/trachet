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

def getchar():
    return _template_char

def getprintablechar():
    return _template_printablechar

def getesc():
    return _template_esc

def getcsi():
    return _template_csi

def getcstr():
    return _template_cstr

def getss2():
    return _template_ss2

def getss3():
    return _template_ss3

def getinvalid():
    return _template_invalid

def getmouse():
    return _template_mouse

def gethighlightmouseinitial():
    return _template_highlight_mouse_initial

def gethighlightmouse():
    return _template_highlight_mouse

def getresize():
    return _template_resize

def getoutputprompt():
    return _template_outputprompt

def getinputprompt():
    return _template_inputprompt

def enable_color():
    global _template_inputprompt
    global _template_outputprompt
    global _template_char
    global _template_printablechar
    global _template_esc
    global _template_csi
    global _template_cstr
    global _template_ss2
    global _template_ss3
    global _template_invalid
    global _template_mouse
    global _template_highlight_mouse_initial
    global _template_highlight_mouse
    global _template_resize

    _template_inputprompt = "\x1b[0;7m<<<"
    _template_outputprompt = "\x1b[m>>>"
    _template_char = ("\x1b[32m" "%s"
                      "\x1b[m")
    _template_printablechar = ("\x1b[31m" "%s"
                               "\x1b[1;32m" "\x0d"
                               "\x1b[30C" "%s"
                               "\x1b[m")
    _template_esc = ("\x1b[0;1;31;44m" " ESC "
                     "\x1b[36m" "%s"
                     "\x1b[33m" "%s "
                     "\x1b[0;1;35m" "\x0d"
                     "\x1b[30C" "%s"
                     "\x1b[m")
    _template_csi = ("\x1b[0;1;31;40m" " CSI "
                     "\x1b[35m" "%s"
                     "\x1b[36m" "%s"
                     "\x1b[33m" "%s "
                     "\x1b[0;1;36m" "\x0d"
                     "\x1b[30C" "%s"
                     "\x1b[m")
    _template_cstr = ("\x1b[0;1;37;44m" " ESC %s "
                      "\x1b[0;1;35m" "%s "
                      "\x1b[37;44m" "ST"
                      "\x1b[0;1;36m" "  %s"
                      "\x1b[m")
    _template_ss2 = ("\x1b[0;1;36;44m" " ESC N " "%s "
		     "\x1b[0;1;31m" "\x0d"
		     "\x1b[30C" "%s")
    _template_ss3 = ("\x1b[0;1;36;44m" " ESC O " "%s "
		     "\x1b[0;1;31m" "\x0d"
		     "\x1b[30C" "%s")
    _template_invalid = ("%s  "
                         "\x1b[33;41m" "%s"
                         "\x1b[m\n")
    _template_mouse = ("%s   "
                       "\x1b[0;1;31m" "CSI "
                       "\x1b[35m" "M "
                       "\x1b[m" "%c %c %c "
                       "\x1b[32;41m" "%s"
                       "\x1b[m\n")
    _template_highlight_mouse_initial = ("%s   "
                                         "\x1b[0;1;31m" "CSI "
                                         "\x1b[35m" "t "
                                         "\x1b[m" "%c %c "
                                         "\x1b[32;41m" "%s"
                                         "\x1b[m\n")
    _template_highlight_mouse = ("%s   "
                                 "\x1b[0;1;31m" "CSI "
                                 "\x1b[35m" "T "
                                 "\x1b[m" "%c %c %c %c %c %c "
                                 "\x1b[32;41m" "%s"
                                 "\x1b[m\n")
    _template_resize = ("%s  "
                        "\x1b[33;41m" " resized: (row=%d, col=%d)"
                        "\x1b[m\n")

def disable_color():
    global _template_inputprompt
    global _template_outputprompt
    global _template_char
    global _template_printablechar
    global _template_esc
    global _template_csi
    global _template_cstr
    global _template_ss2
    global _template_ss3
    global _template_invalid
    global _template_mouse
    global _template_highlight_mouse_initial
    global _template_highlight_mouse
    global _template_resize

    _template_inputprompt = "<<<"
    _template_outputprompt = ">>>"
    _template_char = "%s"
    _template_printablechar = "%s    %s"
    _template_esc = " ESC %s%s    %s"
    _template_csi = " CSI %s%s%s    %s"
    _template_cstr = " ESC %s %s ST  %s"
    _template_ss2 = " ESC N %s   %s"
    _template_ss3 = " ESC N %s   %s"
    _template_invalid = "%s  %s\n"
    _template_mouse = "%s   CSI M %c %c %c %s\n"
    _template_highlight_mouse_initial = "%s   CSI T %c %c %s\n"
    _template_highlight_mouse = "%s   CSI T %c %c %c %c %c %c %s\n"
    _template_resize = "%s   resized: (row=%d, col=%d)\n"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
