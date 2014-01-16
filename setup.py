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

from setuptools import setup, find_packages
from trachet import __version__, __license__, __author__
import inspect
import os

filename = inspect.getfile(inspect.currentframe())
dirpath = os.path.abspath(os.path.dirname(filename))
readmepath = os.path.join(dirpath, "README.rst")

try:
    import trachet.tff
except ImportError:
    print "Please do:\n git submodule update --init"
    import sys
    sys.exit(1)

import trachet.template as template
import trachet.seqdb as seqdb
import trachet.iomode as iomode
import trachet.char as char
import trachet.esc as esc
import trachet.csi as csi
import trachet.cstr as cstr
import trachet.input as input
import trachet.output as output
import trachet.trace as trace
import trachet.controller as controller
import trachet.ss2 as ss2
import trachet.ss3 as ss3
import trachet.constant as constant

import doctest
dirty = False
template.enable_color()
for m in [seqdb, iomode, cstr, char, esc, csi, cstr,
          input, output, controller, ss2, ss3, template,
          trace, constant]:
    failure_count, test_count = doctest.testmod(m)
    if failure_count > 0:
        dirty = True
if dirty:
    raise Exception("test failed.")

setup(name                  = 'trachet',
      version               = __version__,
      description           = 'Provides step-by-step debugging and '
                              'formatted sequence tracing service, '
                              'with terminal applications.',
      long_description      = open(readmepath).read(),
      py_modules            = ['trachet'],
      eager_resources       = [],
      classifiers           = ['Development Status :: 4 - Beta',
                               'Topic :: Terminals',
                               'Environment :: Console',
                               'Intended Audience :: Developers',
                               'License :: OSI Approved :: GNU General Public License (GPL)',
                               'Programming Language :: Python'
                               ],
      keywords              = 'terminal debugger',
      author                = __author__,
      author_email          = 'user@zuse.jp',
      url                   = 'http://saitoha.github.com/trachet',
      license               = __license__,
      packages              = find_packages(exclude=[]),
      zip_safe              = True,
      include_package_data  = False,
#      install_requires      = ['tff >=0.0.15, <0.1.0'],
      install_requires      = [],
      entry_points          = """
                              [console_scripts]
                              trachet = trachet:main
                              """
      )

