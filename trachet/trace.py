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

import codecs, time
import tff

try:
   from cStringIO import StringIO
except:
   from StringIO import StringIO

# formatter
import esc, csi, ss2, ss3, char, cstr
from iomode import IOMode

class SwitchOnOffTrait():
    """
    >>> handler = TraceHandler()
    >>> handler.is_disabled()
    True
    >>> handler.set_disabled()
    >>> handler.is_disabled()
    True
    >>> handler.set_enabled()
    >>> handler.is_disabled()
    False
    """
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
        self.__log = codecs.getwriter(termenc)(StringIO())
        self.__output = output_file
        self.__bufferring = False 
        self._io_mode = IOMode()

    ''' Switch Input/Output prompt state '''

    def set_output(self):
        if self.is_disabled():
            return False
        if self._io_mode.is_input():
            if self.__bufferring:
                self.__log.write("\n")
                self.__bufferring = False
            self._io_mode.set_output() 

    def set_input(self):
        if self.is_disabled():
            return False
        if self._io_mode.is_output():
            if self.__bufferring:
                self.__log.write("\n")
                self.__bufferring = False
            self._io_mode.set_input()

    ''' Override Interface tff.EventObserver '''

    def handle_esc(self, context, intermediate, final):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = esc.format(intermediate, final, self._io_mode.is_input())
        self.__log.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_csi(self, context, parameter, intermediate, final):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = csi.format(parameter, intermediate, final, self._io_mode.is_input())
        self.__log.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_ss2(self, context, final):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = ss2.format(final, self._io_mode.is_input())
        self.__log.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_ss3(self, context, final):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = ss3.format(final, self._io_mode.is_input())
        self.__log.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_control_string(self, context, prefix, value):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = cstr.format(prefix, value, self._io_mode.is_input())
        self.__log.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
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
            self.__log.write("\n")
        else:
            self.__log.write(mnemonic)
        return False # not handled

    def handle_invalid(self, context, seq):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        value = str([hex(c) for c in seq])
        self.__log.write("%s  \x1b[33;41m%s\x1b[0m\n" % (prompt, value))

    def handle_resize(self, context, row, col):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self.__log.write("\n")
            self.__bufferring = False
        prompt = "==="
        self.__log.write("%s  \x1b[33;41m resized: (row=%d, col=%d)\x1b[0m\n" % (prompt, row, col))

    def handle_draw(self, context):
        try:
            self.__output.write(self.__log.getvalue())
        except IOError:
            time.sleep(0.1)
            self.__output.write(self.__log.getvalue())

        try:
            self.__output.flush()
        except IOError:
            time.sleep(0.1)
            self.__output.flush()

        self.__log.truncate(0)

def _test():
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()

