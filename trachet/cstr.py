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

def get_mnemonic(p, v, is_input):

    if is_input:
        direction = '<'
    else:
        direction = '>'

    key = "%s ESC %s%s<ST>" % (direction, p, v)
    if key in _DB:
        return _DB[key]

    if v[0].isalpha():
        key = "%s ESC %s%s<ST>" % (direction, p, v[0])
        if key in _DB:
            return _DB[key]
    else:
        params = v.split(";") 
        length = len(params)

        if length > 3:
            key = "%s ESC %s%s;%s;%s;%s<ST>" % (direction, p, params[0], params[1], params[2], params[3])
            if key in _DB:
                return _DB[key]
        if length > 2:
            key = "%s ESC %s%s;%s;%s<ST>" % (direction, p, params[0], params[1], params[2])
            if key in _DB:
                return _DB[key]
        if length > 1:
            key = "%s ESC %s%s;%s<ST>" % (direction, p, params[0], params[1])
            if key in _DB:
                return _DB[key]
        if length > 0:
            key = "%s ESC %s%s<ST>" % (direction, p, params[0])
            if key in _DB:
                return _DB[key]

    key = "%s ESC %s<ST>" % (direction, p)
    if key in _DB:
        return _DB[key]

    return '[ESC ' + p + ']'

def format(prefix, value, is_input, tracer, controller):
    """
      >>> _create_mock_db() 
      >>> format(ord("]"), map(ord, "abcde"), False, None, None).replace("\x1b", "\\x1b")
      u'\\x1b[0;1;37;44mESC ] \\x1b[0;1;35mabcde \\x1b[37;44mST\\x1b[0;1;36m  OSC / operating system command'

      >>> format(ord("Q"), map(ord, "cdefg"), False, None, None)
      u'\\x1b[0;1;37;44mESC Q \\x1b[0;1;35mcdefg \\x1b[37;44mST\\x1b[0;1;36m  [ESC Q]'
    """

    try:
        v = u''.join(map(unichr, value))
    except OverflowError, e:
        v = str(value)
    p = chr(prefix)

    mnemonic = get_mnemonic(p, v, is_input)
    if mnemonic[0] == "!":
        return eval(mnemonic[1:])

    result = "\x1b[0;1;37;44mESC %s \x1b[0;1;35m%s \x1b[37;44mST\x1b[0;1;36m  %s" % (p, v, mnemonic)
    return result 

def _create_mock_db():
    global _DB
    _DB = {
        '> ESC ]<ST>'        : 'OSC / operating system command',
        '> ESC ]0<ST>'       : 'OSC 0 / set icon name and window title',
        '> ESC ]1<ST>'       : 'OSC 1 / set icon name',
        '> ESC ]2<ST>'       : 'OSC 2 / set window title',
        '> ESC ]4<ST>'       : 'OSC 4 / get or set color palette',
        '> ESC ]9<ST>'       : 'OSC 9 / Growl integration (iTerm2)',
    }
 
if __name__ == "__main__":
   import doctest
   doctest.testmod()

