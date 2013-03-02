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


class InputHandler(tff.DefaultHandler):

    ''' <F6> toggle trace state
        <F7> toggle break state
        <F8> step to next char or seq
        <F9> step to next ESC or CSI seq
    '''

    def __init__(self, controller, tracer):
        self._controller = controller
        self._tracer = tracer 

    def handle_esc(self, context, intermediate, final):
        self._tracer.set_input()
        return self._tracer.handle_esc(context, intermediate, final)

    def handle_csi(self, context, parameter, intermediate, final):
        self._tracer.set_input()
        return self._tracer.handle_csi(context, parameter, intermediate, final)

    def handle_ss2(self, context, final):
        self._tracer.set_input()
        return self._tracer.handle_ss2(context, final)

    def handle_ss3(self, context, final):
        self._tracer.set_input()
        return self._tracer.handle_ss3(context, final)

    def handle_control_string(self, context, prefix, value):
        self._tracer.set_input()
        return self._tracer.handle_control_string(context, prefix, value)

    def handle_char(self, context, final):
        self._tracer.set_input()
        return self._tracer.handle_char(context, final)

    def handle_invalid(self, context, seq):
        self._tracer.set_output()
        return self._tracer.handle_invalid(context, seq)

    def handle_draw(self, context):
        self._controller.tick()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
