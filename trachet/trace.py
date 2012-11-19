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

import codecs
import tff

_CHAR_MAP = ['NUL', 'SOH', 'STX', 'ETX',
             'EOT', 'ENQ', 'ACK', 'BEL',
             'BS',  'HT',  'NL',  'VT',
             'NP',  'CR',  'SO',  'SI', 
             'DLE', 'DC1', 'DC2', 'DC3',
             'DC4', 'NAK', 'SYN', 'ETB',
             'CAN', 'EM',  'SUB', 'ESC',
             'FS',  'GS',  'RS',  'US', 'SP']
_CSI_MAP = {}

def _format_char(c):
   return _CHAR_MAP[c]

def _format_esc(intermediate, final):
    i = ''.join([chr(c) for c in intermediate])
    f = chr(final)
    mnemonic = ''
    
    context = []
    if i:
        context.append("\x1b[36m" + i)
    if f:
        context.append("\x1b[33m" + f)
    result = "\x1b[31;44m ESC %s \x1b[0;32m%s" % (" ".join(context), mnemonic)
    return result


def _format_csi(parameter, intermediate, final):
    p = ''.join([chr(c) for c in parameter])
    i = ''.join([chr(c) for c in intermediate])
    f = chr(final)
    if i == '':
        if f == '@':
            mnemonic = 'ICH'
        elif f == 'A':
            mnemonic = 'CUU'
        elif f == 'B':
            mnemonic = 'CUD'
        elif f == 'C':
            mnemonic = 'CUF'
        elif f == 'D':
            mnemonic = 'CUB'
        elif f == 'E':
            mnemonic = 'CNL'
        elif f == 'F':
            mnemonic = 'CPL'
        elif f == 'G':
            mnemonic = 'CHA'
        elif f == 'H':
            mnemonic = 'CUP'
        elif f == 'I':
            mnemonic = 'CHT'
        elif f == 'J':
            mnemonic = 'ED'
        elif f == 'K':
            mnemonic = 'EL'
        elif f == 'L':
            mnemonic = 'IL'
        elif f == 'M':
            mnemonic = 'DL'
        elif f == 'P':
            mnemonic = 'DCH'
        elif f == 'S':
            mnemonic = 'SU'
        elif f == 'T':
            if p == '':
                mnemonic = 'SD'
            elif p[0] == ">":
                mnemonic = 'Title Mode Setting (xterm)'
            elif p.split(";") > 1:
                mnemonic = 'Initiate Highlight Mouse Tracking (xterm)' 
            else:
                mnemonic = 'SD'
        elif f == 'X':
            mnemonic = 'ECH'
        elif f == 'Z':
            mnemonic = 'CBT'
        elif f == '`':
            mnemonic = 'HPA'
        elif f == 'a':
            mnemonic = 'HPR'
        elif f == 'b':
            mnemonic = 'REP'
        elif f == 'c':
            if p == '':
                mnemonic = 'DA1'
            elif p[0] == '>':
                mnemonic = 'DA2'
            elif p[0] == '?':
                mnemonic = 'DA1 response'
            elif '0' <= p[0] and p[0] <= '9':
                mnemonic = 'DA1'
            else:
                mnemonic = '?'
        elif f == 'd':
            mnemonic = 'VPA'
        elif f == 'e':
            mnemonic = 'VPR'
        elif f == 'f':
            mnemonic = 'HVP'
        elif f == 'g':
            mnemonic = 'TBC'
        elif f == 'h':
            if p == '': #
                mnemonic = 'SM'
            elif parameter[0] == 0x3f: #
                mnemonic = 'DECSET'
            else:
                mnemonic = 'SM'
        elif f == 'i':
            if p == '':
                mnemonic = 'MC'
            elif p[0] == '?':
                mnemonic = 'MC / DEC Specific'
            else:
                mnemonic = 'MC'
        elif f == 'l':
            if p == '': #
                mnemonic = 'RM'
            elif parameter[0] == 0x3f: #
                mnemonic = 'DECRST'
            else:
                mnemonic = 'RM'
        elif f == 'm':
            if p == '':
                mnemonic = 'SGR'
            elif p[0] == '>':
                mnemonic = 'Special Keyboard Modifier Settings (xterm)'
            else:
                mnemonic = 'SGR'
        elif f == 'n':
            if p == '':
                mnemonic = 'DSR'
            elif p[0] == '>':
                mnemonic = 'Disable Special Keyboard Modifier Settings (xterm)'
            elif p[0] == '?':
                mnemonic = 'DSR / DEC Specific'
            else:
                mnemonic = 'DSR'
        elif final == 0x6c: # l
            if parameter[0] == 0x3f: #
                mnemonic = 'DECRST'
            else:
                mnemonic = 'RM'
        elif f == 'r':
            mnemonic = 'DECSTBM'
        else:
            #raise Exception("CSI " + f)
            mnemonic = ''
    else:
        #raise Exception("CSI " + i + " " + f)
        mnemonic = ''
    
    context = []
    if p:
        context.append("\x1b[35m" + p)
    if i:
        context.append("\x1b[36m" + i)
    if f:
        context.append("\x1b[33m" + f)
    result = "\x1b[31;44m CSI %s \x1b[0;36m\x1b[30`%s" % (" ".join(context), mnemonic)
    return result


class TraceHandler(tff.DefaultHandler):

    _direction = ">>>"
    _disabled = False

    def __init__(self, output_file, termenc):
        self.__super = super(TraceHandler, self)
        if isinstance(output_file, str):
            output_file = open(output_file, "w")
        self.__log = codecs.getwriter(termenc)(output_file)
        self.__bufferring = False 
        self._direction = ">>>"

    def set_output(self):
        if self._direction == "\x1b[7m<<<":
            if self.__bufferring:
                self._write('\n')
                self.__bufferring = False
        self._direction = ">>>"

    def is_disabled(self):
        return self._disabled

    def set_disabled(self):
        self._disabled = True

    def set_enabled(self):
        self._disabled = False

    def set_input(self):
        if self.is_disabled():
            return False
        if self._direction == ">>>":
            if self.__bufferring:
                self._write('\n')
                self.__bufferring = False
        self._direction = "\x1b[7m<<<"

    def _write(self, s):
        self.__log.write(s);
        self.__log.flush()

    def handle_csi(self, context, parameter, intermediate, final):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._write('\n')
            self.__bufferring = False
        formatted = _format_csi(parameter, intermediate, final)
        self._write(u"\x1b[0;33m%s  %s\x1b[m\n" % (self._direction, formatted))
        return False # not handled

    def handle_esc(self, context, intermediate, final):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._write('\n')
            self.__bufferring = False
        formatted = _format_esc(intermediate, final)
        self._write(u"\x1b[0;35m%s  %s\x1b[m\n" % (self._direction, formatted))
        return False # not handled

    def handle_control_string(self, context, prefix, value):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._write('\n')
            self.__bufferring = False
        v = ''.join([chr(c) for c in value])
        mnemonic = '[ESC ' + chr(prefix) + ']'
        self._write(u"\x1b[0;36mm%s  \x1b[34m%s \x1b[35m%s\x1b[m\n" % (self._direction, mnemonic, v))
        return False # not handled

    def handle_char(self, context, c):
        if self.is_disabled():
            return False
        if not self.__bufferring:
            self.__bufferring = True
            self._write(u"\x1b[0m%s  " % self._direction)
        if c <= 0x20:
            mnemonic = _format_char(c)
            self._write("\x1b[32m<%s>\x1b[0m" % mnemonic)
        else:
            self._write(unichr(c))
        return False # not handled


