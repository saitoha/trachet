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


def get_mnemonic(direction, prefix, p, i, f):
    '''
      >>> _create_mock_db()
      >>> get_mnemonic('<', '?', '1;2', '', 'c')
      'DA1 Response'
      >>> get_mnemonic('<', '', '32;41;42', '', 'M')
      'urxvt (1015) mouse reporting (code=(32-32),row=41,col=42)'
    '''

    params = p.split(";")

    if len(p) == 0 or len(p) == len(prefix):
        length = 0
    else:
        key = '%s CSI %s%s%s' % (direction, p, i, f)
        if key in _DB:
            return _DB[key]
        length = len(params)

#    if length > 0:
#        key = '%s CSI %s;[*]%s%s' % (direction, params[0], i, f)
#        if key in _DB:
#            return _DB[key]

    key = '%s CSI %s[%s]%s%s' % (direction, prefix, length, i, f)
    if key in _DB:
        if length > 0:
            return _DB[key] % tuple(params)
        else:
            return _DB[key]

    if length > 1:
        for x in xrange(0, length):
            pbytes = ";".join(params[:x])
            key = '%s CSI %s;[%s]%s%s' % (direction, pbytes, length - x, i, f)
            if key in _DB:
                return _DB[key] % tuple(params[x:])

    key = '%s CSI %s%s%s' % (direction, prefix, i, f)
    if key in _DB:
        return _DB[key]
    return '<Unknown>'


def format(parameter, intermediate, final, is_input, tracer, controller):
    '''
      >>> _create_mock_db()
      >>> template.disable_color()
      >>> format([0x3f, 0x31, 0x3b, 0x32], [], 0x63, True, None, None)
      ' CSI ?1;2c    DA1 Response'
    '''

    p = ''.join([chr(c) for c in parameter])
    i = ''.join([chr(c) for c in intermediate]).replace(" ", "<SP>")
    f = chr(final)

    if is_input:
        direction = '<'
    else:
        direction = '>'

    if p and p[0] > ";":
        prefix = p[0]
    else:
        prefix = ''

    mnemonic = get_mnemonic(direction, prefix, p, i, f)
    if mnemonic[0] == "!":
        return eval(mnemonic[1:])

    return template.getcsi() % (p, i, f, mnemonic)


def _create_mock_db():
    global _DB
    _DB = {
        '< CSI A': 'Cursor key(normal keypad): up arrow',
        '< CSI 1;5A': 'Cursor key (xterm): Ctrl + up arrow',
        '< CSI [0]M': 'xterm normal mouse reporting, '
                      'following 3 bytes mean (code, row, col)',
        '< CSI [3]M': 'urxvt (1015) mouse reporting '
                      '(code=(%s-32),row=%s,col=%s)',
        '< CSI ?c': 'DA1 Response',
        '< CSI >0;95;c': 'DA2 Response: xterm patch#95 '
                         '(could be iTerm/iTerm2)',
        '> CSI @': 'ICH / insert blank characters',
        '> CSI [2]H': 'CUP / move cursor to (row=%s, col=%s)',
        '> CSI >2T': 'Title Mode - Reset (xterm) 2:'
                     ' Do not set window/icon labels using UTF-8',
    }

if __name__ == "__main__":
    import doctest
    doctest.testmod()
