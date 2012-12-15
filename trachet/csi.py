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

def get_mnemonic(direction, prefix, p, i, f):

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

    key = '%s CSI %s[%d]%s%s' % (direction, prefix, length, i, f)
    if key in _DB:
        if length > 0:
            return _DB[key] % tuple(params)
        else:
            return _DB[key]

    if length > 1:
        for x in xrange(0, length):
            key = '%s CSI %s;[%d]%s%s' % (direction, ";".join(params[:x]), length - x, i, f)
            if key in _DB:
                return _DB[key] % tuple(params[x:]) 

    key = '%s CSI %s%s%s' % (direction, prefix, i, f)
    if key in _DB:
        return _DB[key] 
    return '<Unknown>'
 
def format(parameter, intermediate, final, is_input, tracer, controller):
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
   
    context = []
    if p:
        context.append("\x1b[35m" + p)
    if i:
        context.append("\x1b[36m" + i)
    if f:
        context.append("\x1b[33m" + f)

    result = "\x1b[0;1;31;40m CSI %s \x1b[0;1;36m\x0d\x1b[30C%s" % (" ".join(context), mnemonic)
    return result

 
if __name__ == "__main__":
   import doctest
   doctest.testmod()

