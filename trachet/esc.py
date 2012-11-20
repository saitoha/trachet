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


_ISO_2022_FBYTE_MAP = {
    '0': 'DEC Special Character and Line Drawing Set',
    'A': 'United Kingdom (UK)',
    'B': 'United States (USASCII)',
    '4': 'Dutch',
    'C': 'Finnish',
    '5': 'Finnish',
    'R': 'French',
    'Q': 'French Canadian',
    'K': 'German',
    'I': 'Italian',
    'E': 'Norwegian/Danish',
    '6': 'Norwegian/Danish',
    'Z': 'Spanish',
    'H': 'Swedish',
    '7': 'Swedish',
    '=': 'Swiss',
}

_ESC_MAP = {
    '/6': 'DECBI',
    '/7': 'DECSC',
    '/8': 'DECRC',
    '/9': 'DECFI',
    '/=': 'DECKPAM',
    '/>': 'DECKPNM',
    '<SP>/F': 'S7C1T',
    '<SP>/G': 'S8C1T',
    '<SP>/L': 'Set ANSI conformance level 1',
    '<SP>/M': 'Set ANSI conformance level 2',
    '<SP>/N': 'Set ANSI conformance level 3',
    '#/3': 'DECDHLT',
    '#/4': 'DECDHLB',
    '#/5': 'DECSWL',
    '#/6': 'DECDWL',
    '#/8': 'DECALN',
    '%/@': 'Select default character set',
    '%/G': 'Select UTF-8 character set',
}

def format(intermediate, final):
    i = ''.join([chr(c) for c in intermediate]).replace(" ", "<SP>")
    f = chr(final)
    key = "/".join((i, f))
    if key in _ESC_MAP:
        mnemonic = _ESC_MAP[key]
    elif i == '(':
        if f in _ISO_2022_FBYTE_MAP:
            mnemonic = _ISO_2022_FBYTE_MAP[f]
        else:
            mnemonic = 'Unknown Final Byte - ' + f
        mnemonic = 'G0 -> ' + mnemonic
    else: 
        mnemonic = '<Unknown>'

    context = []
    if i:
        context.append("\x1b[36m" + i)
    if f:
        context.append("\x1b[33m" + f)
    result = "\x1b[0;1;31;44m ESC %s \x1b[0;1;35m\x0d\x1b[30C%s" % (" ".join(context), mnemonic)
    return result


