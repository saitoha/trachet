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


_CHAR_MAP = ['NUL', 'SOH', 'STX', 'ETX',
             'EOT', 'ENQ', 'ACK', 'BEL',
             'BS',  'HT',  'NL',  'VT',
             'NP',  'CR',  'SO',  'SI', 
             'DLE', 'DC1', 'DC2', 'DC3',
             'DC4', 'NAK', 'SYN', 'ETB',
             'CAN', 'EM',  'SUB', 'ESC',
             'FS',  'GS',  'RS',  'US', 'SP']

def format(c):
   return _CHAR_MAP[c]

