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

import seqdb, controller

_DB = seqdb.get()

def get_mnemonic(direction, f):
    key = "%s ESC O %s" % (direction, f)
    if key in _DB:
        mnemonic = _DB[key]
    else: 
        mnemonic = '<Unknown>'
    return mnemonic

def format(final, is_input, tracer, controller):
    f = chr(final)

    if is_input:
        direction = '<'
    else:
        direction = '>'

    mnemonic = get_mnemonic(direction, f) 
    if mnemonic[0] == "!":
        eval(mnemonic[1:])
        return None

    context = []
    if f:
        context.append("\x1b[33m" + f)
    result = "\x1b[0;1;36;44m ESC O %s \x1b[0;1;31m\x0d\x1b[30C%s" % (" ".join(context), mnemonic)
    return result

 
if __name__ == "__main__":
   import doctest
   doctest.testmod()

