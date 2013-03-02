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


_DEBUG_MODE_NONE = 0
_DEBUG_MODE_NORMAL_STEP = 1
_DEBUG_MODE_FUZZY_STEP = 2
_DEBUG_MODE_STOP = 3

import constant
import time


class ActionController():

    __mode = _DEBUG_MODE_NONE
    __actions = None
    __accel = 1.0
    __lastcalltime = 0

    def __init__(self, tty):
        self.__mode = _DEBUG_MODE_NONE
        self.__actions = []
        self.__tty = tty
        self.__accel = 1.0

    def is_suspended(self):
        return self.__mode != _DEBUG_MODE_NONE

    def append(self, action):
        return self.__actions.append(action)

    def resume(self):
        self.__mode = _DEBUG_MODE_NONE
        #self.__tty.xon()

    def set_normal_step(self):
        self.__mode = _DEBUG_MODE_NORMAL_STEP

    def set_fuzzy_step(self):
        self.__mode = _DEBUG_MODE_FUZZY_STEP

    def set_break(self):
        self.__mode = _DEBUG_MODE_STOP
        #self.__tty.xoff()

    def _get_repeat_count(self):
        now = time.time()
        if now - self.__lastcalltime < 0.1:
            self.__accel *= 1.2
        else:
            self.__accel = 1
        self.__lastcalltime = now

        repeat = max(1, self.__accel)

        return repeat

    def tick(self):
        if self.__mode == _DEBUG_MODE_NONE:
            while self.__actions:
                action = self.__actions.pop(0)
                result = action()

        elif self.__mode == _DEBUG_MODE_NORMAL_STEP:
            self.__mode = _DEBUG_MODE_STOP
            repeat = self._get_repeat_count()
            while repeat > 0 and self.__actions:
                repeat -= 1
                action = self.__actions.pop(0)
                result = action()

        elif self.__mode == _DEBUG_MODE_FUZZY_STEP:
            self.__mode = _DEBUG_MODE_STOP
            repeat = self._get_repeat_count()
            while repeat > 0:
                repeat -= 1
                while self.__actions:
                    action = self.__actions.pop(0)
                    result = action()
                    if result != constant.SEQ_TYPE_CHAR:
                        break
                else:
                    return


if __name__ == "__main__":
    import doctest
    doctest.testmod()
