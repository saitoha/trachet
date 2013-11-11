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

__author__ = "Hayaki Saito (user@zuse.jp)"
__version__ = "0.3.2"
__license__ = "GPL v3"
__doc__ = """
This program runs as a terminal filter process between terminals and applications.
It provides step-by-step debugging and formatted sequence tracing service.
You can watch terminal I/O sequence on realtime, and it enables you to do step-by-step execution.

Most of terminal applications such as vi have single threaded UI and typically has blocking terminal I/O.
So trachet might be useful for both of terminal emulator developers and terminal application developers.
"""

from trachet import *
