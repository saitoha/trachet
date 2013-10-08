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

import tff
import constant


class OutputHandler(tff.DefaultHandler):

    def __init__(self, controller, tracer):
        self._tracer = tracer
        self._controller = controller

    def handle_csi(self, context, parameter, intermediate, final):
        def action():
            context.put(0x1b)  # ESC
            context.put(0x5b)  # [
            for c in parameter:
                context.put(c)
            for c in intermediate:
                context.put(c)
            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_csi(context, parameter, intermediate, final)
            return constant.SEQ_TYPE_CSI
        self._controller.append(action)
        return True  # handled

    def handle_esc(self, context, intermediate, final):
        def action():
            context.put(0x1b)  # ESC
            for c in intermediate:
                context.put(c)
            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_esc(context, intermediate, final)
            return constant.SEQ_TYPE_ESC
        self._controller.append(action)
        return True  # handled

    def handle_ss2(self, context, final):
        def action():
            context.put(0x1b)  # ESC
            context.put(0x4e)  # N
            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_ss2(context, final)
            return constant.SEQ_TYPE_SS2
        self._controller.append(action)
        return True  # handled

    def handle_ss3(self, context, final):
        def action():
            context.put(0x1b)  # ESC
            context.put(0x4f)  # O
            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_ss3(context, final)
            return constant.SEQ_TYPE_SS3
        self._controller.append(action)
        return True  # handled

    def handle_control_string(self, context, prefix, value):
        def action():
            context.put(0x1b)  # ESC
            context.put(prefix)
            for c in value:
                context.put(c)
            context.put(0x1b)  # ESC
            context.put(0x5c)  # \
            self._tracer.set_output()
            self._tracer.handle_control_string(context, prefix, value)
            return constant.SEQ_TYPE_STR
        self._controller.append(action)
        return True

    def handle_char(self, context, final):
        def action():
            context.put(final)
            self._tracer.set_output()
            self._tracer.handle_char(context, final)
            return constant.SEQ_TYPE_CHAR
        self._controller.append(action)
        return True  # handled

    def handle_invalid(self, context, seq):
        def action():
            for c in seq:
                context.put(c)
            self._tracer.set_output()
            self._tracer.handle_invalid(context, seq)
            return constant.SEQ_TYPE_CHAR
        self._controller.append(action)
        return True  # handled

    def handle_resize(self, context, row, col):
        self._tracer.handle_resize(context, row, col)

    def handle_draw(self, context):
        self._controller.tick()
        self._tracer.handle_draw(context)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
