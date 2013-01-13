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
except ImportError:
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
    _xterm_mouse_buffer = None 

    def __init__(self, output_file, termenc, controller):
        if isinstance(output_file, str):
            output_file = open(output_file, "w")
        self._buffer = codecs.getwriter(termenc)(StringIO())
        self._output = output_file
        self.__bufferring = False 
        self._controller = controller
        self._io_mode = IOMode()

    ''' Switch Input/Output prompt state '''

    def set_output(self):
        if self.is_disabled():
            return
        if self._io_mode.is_input():
            if self.__bufferring:
                self._buffer.write("\n")
                self.__bufferring = False
            self._io_mode.set_output() 

    def set_input(self):
        if self.is_disabled():
            return
        if self._io_mode.is_output():
            if self.__bufferring:
                self._buffer.write("\n")
                self.__bufferring = False
            self._io_mode.set_input()

    ''' Override Interface tff.EventObserver '''

    def handle_esc(self, context, intermediate, final):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = [ 0x1b, 0x5b, 0x4d ] + self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None 
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = esc.format(intermediate,
                               final,
                               self._io_mode.is_input(),
                               self,
                               self._controller)
        if not formatted:
            return True
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        self._buffer.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_csi(self, context, parameter, intermediate, final):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = [ 0x1b, 0x5b, 0x4d ] + self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None 
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = csi.format(parameter,
                               intermediate,
                               final,
                               self._io_mode.is_input(),
                               self,
                               self._controller)
        if final == 0x4d:
            if not parameter:
                if not intermediate:
                    self._xterm_mouse_buffer = []
                    return False
        if not formatted:
            return True
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        self._buffer.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_ss2(self, context, final):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = [ 0x1b, 0x5b, 0x4d ] + self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None 
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = ss2.format(final,
                               self._io_mode.is_input(),
                               self,
                               self._controller)
        if not formatted:
            return True
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        self._buffer.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_ss3(self, context, final):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = [ 0x1b, 0x5b, 0x4d ] + self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None 
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = ss3.format(final,
                               self._io_mode.is_input(),
                               self,
                               self._controller)
        if not formatted:
            return True
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        self._buffer.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_control_string(self, context, prefix, value):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = [ 0x1b, 0x5b, 0x4d ] + self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None 
            self.handle_invalid(context, seq)
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        formatted = cstr.format(prefix,
                                value,
                                self._io_mode.is_input(),
                                self,
                                self._controller)
        if not formatted:
            return True
        self._buffer.write(u"%s  %s\x1b[m\n" % (prompt, formatted))
        return False # not handled

    def handle_char(self, context, c):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            self._xterm_mouse_buffer.append(c) 
            if len(self._xterm_mouse_buffer) == 3:
                seq = self._xterm_mouse_buffer
                self._xterm_mouse_buffer = None
                self.handle_xterm_mouse(context, seq)
            return False
        mnemonic, handled = char.format(c,
                                        self._io_mode.is_input(),
                                        self,
                                        self._controller)
        if not mnemonic:
            return True
        if self.is_disabled():
            return False
        if not self.__bufferring:
            self.__bufferring = True
            prompt = self._io_mode.get_prompt()
            self._buffer.write(u"%s  " % prompt)
        if handled:
            self.__bufferring = False
            self._buffer.write(mnemonic)
            self._buffer.write("\n")
        else:
            self._buffer.write(mnemonic)
        return False # not handled

    def handle_invalid(self, context, seq):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = [ 0x1b, 0x5b, 0x4d ] + self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None 
            self.handle_invalid(context, seq)
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        value = str([hex(c) for c in seq])
        self._buffer.write("%s  \x1b[33;41m%s\x1b[0m\n" % (prompt, value))

    def handle_xterm_mouse(self, context, seq):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        info = (seq[0] - 32, seq[1] - 32, seq[2] - 32)
        value = "xterm normal mouse: button=%d, row=%d, col=%d" % info
        self._buffer.write("%s   \x1b[0;1;31mCSI \x1b[35mM \x1b[m%c %c %c \x1b[32;41m%s\x1b[0m\n" % (prompt, seq[0], seq[1], seq[2], value))
        pass

    def handle_resize(self, context, row, col):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        prompt = "==="
        self._buffer.write("%s  \x1b[33;41m resized: (row=%d, col=%d)\x1b[0m\n" % (prompt, row, col))

    def handle_draw(self, context):
        try:
            self._output.write(self._buffer.getvalue())
        except IOError:
            time.sleep(0.1)
            self._output.write(self._buffer.getvalue())
        try:
            self._output.flush()
        except IOError:
            time.sleep(0.1)
            self._output.flush()

        self._buffer.truncate(0)

def _test():
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()

