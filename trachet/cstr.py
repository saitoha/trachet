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

def format(prefix, value, is_input):
    v = u''.join([unichr(c) for c in value])
    p = chr(prefix)

    if is_input:
        direction = '<'
    else:
        direction = '>'

    key = "%s ESC %s<ST>" % (direction, p)
    if key in _DB:
        mnemonic = _DB[key]
    else:
        mnemonic = '[ESC ' + chr(prefix) + ']'
    result = "\x1b[0;1;37;44mESC %s \x1b[0;1;35m%s \x1b[37;44mST\x1b[0;1;36m  %s" % (p, v, mnemonic)
    return result 


