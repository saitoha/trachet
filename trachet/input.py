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

    def __init__(self, actions, tracer):
        self.__actions = actions
        self.__tracer = tracer 

    def _handle_fkeys(self, parameter, intermediate, final):
        if final == 0x7e and len(intermediate) == 0: # final byte is "~"
            if parameter == [0x31, 0x37]:   # F6 / CSI 17~
                if self.__tracer.is_disabled():
                    self.__tracer.set_enabled()
                else: 
                    self.__tracer.set_disabled()
                return True
            elif parameter == [0x31, 0x38]:   # F8 / CSI 18~
                if self.__actions.is_suspended():
                    self.__actions.resume()
                else:
                    self.__actions.set_break()
                return True
            elif self.__actions.is_suspended():
                if parameter == [0x31, 0x39]: # F9 / CSI 19~
                    self.__actions.set_normal_step()
                    return True
                elif parameter == [0x32, 0x30]: # F10 / CSI 20~
                    self.__actions.set_fuzzy_step()
                    return True
        return False

    def handle_csi(self, context, parameter, intermediate, final):
        if self._handle_fkeys(parameter, intermediate, final):
            return True
        self.__tracer.set_input()
        self.__tracer.handle_csi(context, parameter, intermediate, final)
        return False 

    def handle_esc(self, context, intermediate, final):
        self.__tracer.set_input()
        self.__tracer.handle_esc(context, intermediate, final)
        return False 

    def handle_control_string(self, context, prefix, value):
        self.__tracer.set_input()
        self.__tracer.handle_control_string(context, prefix, value)
        return False 

    def handle_char(self, context, final):
        self.__tracer.set_input()
        self.__tracer.handle_char(context, final)
        return False 

    def handle_draw(self, context):
        self.__actions.tick()


