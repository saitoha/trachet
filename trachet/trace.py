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

# formatter
import esc
import csi
import char
import cstr
from iomode import IOMode

class SwitchOnOffTrait():

    _disabled = False

    def is_disabled(self):
        return self._disabled

    def set_disabled(self):
        self._disabled = True

    def set_enabled(self):
        self._disabled = False


class TraceHandler(tff.DefaultHandler, SwitchOnOffTrait):

    _io_mode = None

    def __init__(self, output_file, termenc, use_header):
        self.__super = super(TraceHandler, self)
        if isinstance(output_file, str):
            output_file = open(output_file, "w")
        self.__log = codecs.getwriter(termenc)(output_file)
        self.__log.write("\x1bcHello!")
        if use_header:
            self.__log.write("\x1b[1;2r") 
        self.__bufferring = False 
        self._io_mode = IOMode()

    ''' Switch Input/Output prompt state '''

    def set_output(self):
        if self.is_disabled():
            return False
        if self._io_mode.is_input():
            if self.__bufferring:
                self.__log.write('\n')
                self.__bufferring = False
            self._io_mode.set_output() 

    def set_input(self):
        if self.is_disabled():
            return False
        if self._io_mode.is_output():
            if self.__bufferring:
                self.__log.write('\n')
                self.__bufferring = False
            self._io_mode.set_input()

    ''' Override Interface tff.EventObserver '''

    def handle_csi(self, context, parameter, intermediate, final):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write('\n')
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = csi.format(parameter, intermediate, final, self._io_mode.is_input())
        self.__log.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        self.__log.flush()
        return False # not handled

    def handle_esc(self, context, intermediate, final):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write('\n')
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = esc.format(intermediate, final, self._io_mode.is_input())
        self.__log.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        self.__log.flush()
        return False # not handled

    def handle_control_string(self, context, prefix, value):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write('\n')
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = cstr.format(prefix, value, self._io_mode.is_input())
        self.__log.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        self.__log.flush()
        return False # not handled

    def handle_char(self, context, c):
        if self.is_disabled():
            return False
        if not self.__bufferring:
            self.__bufferring = True
            prompt = self._io_mode.get_prompt()
            self.__log.write(u"%s  " % prompt)
        mnemonic, handled = char.format(c, self._io_mode.is_input())
        if handled:
            self.__bufferring = False
            self.__log.write(mnemonic)
            self.__log.write('\n')
        else:
            self.__log.write(mnemonic)
        self.__log.flush()
        return False # not handled


