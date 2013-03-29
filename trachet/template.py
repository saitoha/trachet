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

def getinvalid():
    return _template_invalid

def enable_color():
    global _template_char
    global _template_printablechar
    global _template_esc
    global _template_csi
    global _template_cstr
    global _template_invalid

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

def disable_color():
    global _template_char
    global _template_printablechar
    global _template_esc
    global _template_csi
    global _template_cstr
    global _template_invalid
    _template_char = "%s"
    _template_printablechar = "%s    %s"
    _template_esc = " ESC %s%s    %s"
    _template_csi = " CSI %s%s%s    %s"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
