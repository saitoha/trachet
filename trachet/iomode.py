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


_DIRECTION_INPUT  = True
_DIRECTION_OUTPUT = False
_PROMPT_INPUT     = "\x1b[0;7m<<<"
_PROMPT_OUTPUT    = "\x1b[0m>>>"

class IOMode():

    _direction = _DIRECTION_INPUT 

    def is_input(self):
        return self._direction == _DIRECTION_INPUT

    def is_output(self):
        return self._direction == _DIRECTION_OUTPUT

    def set_input(self):
        self._direction = _DIRECTION_INPUT

    def set_output(self):
        self._direction = _DIRECTION_OUTPUT

    def get_prompt(self):
        if self.is_input():
            return _PROMPT_INPUT
        return _PROMPT_OUTPUT


