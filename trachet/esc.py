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
import template

_DB = seqdb.get()


def get_mnemonic(direction, i, f):
    key = "%s ESC %s%s" % (direction, i, f)
    if key in _DB:
        mnemonic = _DB[key]
    else:
        mnemonic = '<Unknown>'
    return mnemonic


def format(intermediate, final, is_input, tracer, controller):
    i = ''.join([chr(c) for c in intermediate]).replace(" ", "<SP>")
    f = chr(final)

    if is_input:
        direction = '<'
    else:
        direction = '>'

    mnemonic = get_mnemonic(direction, i, f)
    if mnemonic[0] == "!":
        return eval(mnemonic[1:])

    return template.getesc() % (i, f, mnemonic)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
