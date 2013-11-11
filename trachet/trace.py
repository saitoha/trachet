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
import time
import tff
import template

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

# formatter
import esc
import csi
import ss2
import ss3
import char
import cstr
from iomode import IOMode


class MockController():
    pass

class SwitchOnOffTrait():
    """
    >>> controller = MockController
    >>> output_file = StringIO()
    >>> handler = TraceHandler(output_file, "utf-8", controller)
    >>> handler.is_disabled()
    False
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
    _xterm_mouse_counter = 0

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
            seq = self._xterm_mouse_buffer
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
        self._buffer.write(u"%s  %s\n" % (prompt, formatted))
        return False  # not handled

    def handle_csi(self, context, parameter, intermediate, final):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None
            self.handle_invalid(context, seq)
        prompt = self._io_mode.get_prompt()
        formatted = csi.format(parameter,
                               intermediate,
                               final,
                               self._io_mode.is_input(),
                               self,
                               self._controller)
        if final == 0x4d or final == 0x54 or final == 0x74:  # 'M' or 'T' or 't'
            if self._io_mode.is_input():
                if not parameter:
                    if not intermediate:
                        self._xterm_mouse_buffer = [0x1b, 0x5b, final]
                        self._xterm_mouse_counter = { 0x4d: 3, 0x74: 2, 0x54: 6 }[final]
                        return False
        if not formatted:
            return True
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        self._buffer.write(u"%s  %s\n" % (prompt, formatted))
        return False  # not handled

    def handle_ss2(self, context, final):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
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
        self._buffer.write(u"%s  %s\n" % (prompt, formatted))
        return False  # not handled

    def handle_ss3(self, context, final):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
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
        self._buffer.write(u"%s  %s\n" % (prompt, formatted))
        return False  # not handled

    def handle_control_string(self, context, prefix, value):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
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
        self._buffer.write(u"%s  %s\n" % (prompt, formatted))
        return False  # not handled

    def handle_char(self, context, c):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            buf = self._xterm_mouse_buffer
            buf.append(c)
            self._xterm_mouse_counter -= 1;
            buflen = len(buf)
            if self._xterm_mouse_counter == 0:
                self._xterm_mouse_buffer = None
                self.handle_xterm_mouse(context, buf)
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
        return False  # not handled

    def handle_invalid(self, context, seq):
        if not self._xterm_mouse_buffer is None and self._io_mode.is_input():
            seq = self._xterm_mouse_buffer
            self._xterm_mouse_buffer = None
            self.handle_invalid(context, seq)
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        value = str([hex(c) for c in seq])
        template_invalid = template.getinvalid()
        self._buffer.write(template_invalid % (prompt, value))

    def handle_xterm_mouse(self, context, seq):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        prompt = self._io_mode.get_prompt()
        if seq[2] == 0x4d:  # M
            info = (seq[3] - 32, seq[4] - 32, seq[5] - 32)
            value = "xterm normal mouse: button=%d, x=%d, y=%d" % info
            self._buffer.write(template.getmouse() % (prompt,
                                                      seq[3], seq[4], seq[5],
                                                      value))
        elif seq[2] == 0x74:  # t
            info = (seq[3] - 32, seq[4] - 32)
            value = "xterm highlight mouse: x=%d, y=%d" % info
            self._buffer.write(template.gethighlightmouseinitial() % (prompt,
                                                                      seq[3], seq[4],
                                                                      value))
        elif seq[2] == 0x54:  # T
            info = (seq[3] - 32, seq[4] - 32, seq[5] - 32, seq[6] - 32, seq[7] - 32, seq[8] - 32)
            value = "xterm highlight mouse: startx=%d starty=%d, endx=%d, endy=%d, mousex=%d, mousey=%d" % info
            self._buffer.write(template.gethighlightmouse() % (prompt,
                                                               seq[3], seq[4], seq[5], seq[6], seq[7], seq[8],
                                                               value))

    def handle_resize(self, context, row, col):
        if self.is_disabled():
            return False
        if self.__bufferring:
            self._buffer.write("\n")
            self.__bufferring = False
        prompt = "==="
        self._buffer.write(template.getresize() % (prompt, row, col))

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
