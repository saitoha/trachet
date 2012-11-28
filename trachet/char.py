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

import seqdb

_DB = seqdb.get()

_CHAR_MAP = {0x00: '<NUL>',
             0x01: '<SOH>',
             0x02: '<STX>',
             0x03: '<ETX>',
             0x04: '<EOT>',
             0x05: '<ENQ>',
             0x06: '<ACK>',
             0x07: '<BEL>',
             0x08: '<BS>',
             0x09: '<HT>',
             0x0A: '<NL>',
             0x0B: '<VT>',
             0x0C: '<NP>',
             0x0D: '<CR>',
             0x0E: '<SO>',
             0x0F: '<SI>', 
             0x10: '<DLE>',
             0x11: '<DC1>',
             0x12: '<DC2>',
             0x13: '<DC3>',
             0x14: '<DC4>',
             0x15: '<NAK>',
             0x16: '<SYN>',
             0x17: '<ETB>',
             0x18: '<CAN>',
             0x19: '<EM>',
             0x1A: '<SUB>',
             0x1B: '<ESC>',
             0x1C: '<FS>',
             0x1D: '<GS>',
             0x1E: '<RS>',
             0x1F: '<US>',
             0x20: '<SP>',
             0x7F: '<DEL>'}

def format(c, is_input):
    if _CHAR_MAP.has_key(c):
        printable_char = _CHAR_MAP[c]
    else:
        printable_char = unichr(c) 

    if is_input:
        direction = '<'
    else:
        direction = '>'

    key = "%s %s" % (direction, printable_char)

    if _DB.has_key(key):
        return u"\x1b[31m%s\x1b[1;32m\x0d\x1b[30C%s" % (printable_char, _DB[key]), True
    return u"\x1b[32m%s" % printable_char, False

