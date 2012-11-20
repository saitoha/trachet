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


_CSI_MAP={
    '//@': 'ICH',
    '//A': 'CUU',
    '//B': 'CUD',
    '//C': 'CUF',
    '//D': 'CUB',
    '//E': 'CNL',
    '//F': 'CPL',
    '//G': 'CHA',
    '//H': 'CUP',
    '//I': 'CHT',
    '//J': 'ED',
    '//K': 'EL',
    '//L': 'IL',
    '//M': 'DL',
    '<//M': 'SGR (1006) Mouse Reporting / Button Up',
    '//P': 'DCH',
    '//R': 'DSR 6 (cursor position) Response',
    '//S': 'SU',
    '//X': 'ECH',
    '//Z': 'CBT',
    '//`': 'HPA',
    '//a': 'HPR',
    '//b': 'REP',
    '//c': 'DA1',
    '>//c': 'DA2',
    '?//c': 'DA1 Response',
    '//d': 'VPA',
    '//e': 'VPR',
    '//f': 'HVP',
    '//g': 'TBC',
    '//h': 'SM',
    '?//h': 'DECSET',
    '//i': 'MC',
    '?//i': 'MC / DEC Specific',
    '//l': 'RM',
    '?//l': 'DECRST',
    '//m': 'SGR',
    '<//m': 'SGR (1006) Mouse Reporting',
    '>//m': 'Special Keyboard Modifier Settings (xterm)',
    '//n': 'DSR',
    '?//n': 'DSR / DEC Specific',
    '>//n': 'Disable Special Keyboard Modifier Settings (xterm)',
    '//r': 'DECSTBM',
    '//t': 'DECSLPP or Window Manipulation (dtterm)'
}

def format(parameter, intermediate, final):
    p = ''.join([chr(c) for c in parameter])
    i = ''.join([chr(c) for c in intermediate]).replace(" ", "<SP>")
    f = chr(final)
    if p and p[0] > ";":
        prefix = p[0]
    else:
        prefix = ''
    key = '/'.join((prefix, i, f))
    if i == '':
        if key in _CSI_MAP:
            mnemonic = _CSI_MAP[key] 
        elif f == 'T':
            if p == '':
                mnemonic = 'SD'
            elif p[0] == ">":
                mnemonic = 'Title Mode Setting (xterm)'
            elif p.split(";") > 1:
                mnemonic = 'Initiate Highlight Mouse Tracking (xterm)' 
            else:
                mnemonic = 'SD'
        else:
            #raise Exception("CSI " + f)
            mnemonic = '<Unknown>'
    else:
        #raise Exception("CSI " + i + " " + f)
        mnemonic = '<Unknown>'
    
    context = []
    if p:
        context.append("\x1b[35m" + p)
    if i:
        context.append("\x1b[36m" + i)
    if f:
        context.append("\x1b[33m" + f)
    result = "\x1b[0;1;31;40m CSI %s \x1b[0;1;36m\x0d\x1b[30C%s" % (" ".join(context), mnemonic)
    return result


