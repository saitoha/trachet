#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012-2014  Hayaki Saito <user@zuse.jp>
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
    >>> _create_mock_db()
    >>> get_mnemonic('<', 'A')
    'Cursor key(application keypad): up arrow'
    >>> get_mnemonic('>', 'B')
    '<unknown>'
    >>> get_mnemonic('<', '[')
    'alternate escape key'
    """
    key = "%s ESC O %s" % (direction, f)
    if key in _DB:
        mnemonic = _DB[key]
    else:
        mnemonic = '<unknown>'
    return mnemonic

def format(final, is_input, tracer, controller):
    """
    >>> _create_mock_db()
    >>> template.enable_color()
    >>> format(0x42, True, None, None)
    '\\x1b[0;1;36;44m ESC O B \\x1b[0;1;31m\\r\\x1b[30CCursor key(application keypad): down arrow'
    >>> template.disable_color()
    >>> format(0x42, True, None, None)
    ' ESC O B   Cursor key(application keypad): down arrow'
    >>> format(0x42, False, None, None)
    ' ESC O B   <unknown>'
    >>> import sys
    >>> format(0x74, True, sys, None)
    test
    """
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
        context.append(f)
    result = template.getss3() % (" ".join(context), mnemonic)
    return result


def _test():
    """
    >>> _test()
    test
    <unknown>
    """
    global _DB
    _DB = {'> ESC O O': 'test'}

    print get_mnemonic('>', 'O')

    print get_mnemonic('>', 'A')

def _create_mock_db():
    global _DB
    _DB = {
        '> ESC O'   : 'SS3',
        '< ESC O'   : 'SS3',
        '< ESC O A' : 'Cursor key(application keypad): up arrow',
        '< ESC O B' : 'Cursor key(application keypad): down arrow',
        '< ESC O C' : 'Cursor key(application keypad): right arrow',
        '< ESC O D' : 'Cursor key(application keypad): left arrow',
        '< ESC O P' : 'F1 key (xterm)',
        '< ESC O Q' : 'F2 key (xterm)',
        '< ESC O R' : 'F3 key (xterm)',
        '< ESC O S' : 'F4 key (xterm)',
        '< ESC O t' : '!tracer.stdout.write("test")',
        '< ESC O [' : 'alternate escape key',
    }


if __name__ == "__main__":
    import doctest
    doctest.testmod()
