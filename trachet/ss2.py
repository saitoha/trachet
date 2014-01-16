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


def get_mnemonic(direction, f):
    """
    >>> get_mnemonic('=', 'O')
    '<unknown>'
    """

    key = "%s ESC N %s" % (direction, f)
    if key in _DB:
        mnemonic = _DB[key]
    else:
        mnemonic = '<unknown>'
    return mnemonic


def format(final, is_input, tracer, controller):
    f = chr(final)

    if is_input:
        direction = '<'
    else:
        direction = '>'

    mnemonic = get_mnemonic(direction, f)
    if mnemonic[0] == "!":
        return eval(mnemonic[1:])

    context = []
    if f:
        context.append(f)
    result = template.getss2() % (" ".join(context), mnemonic)
    return result


def _test():
    """
    >>> _test()
    test
    <unknown>
    """
    global _DB
    _DB = {'> ESC N O': 'test'}

    print get_mnemonic('>', 'O')

    print get_mnemonic('>', 'A')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
