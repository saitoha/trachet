# -*- coding: utf-8 -*-

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

import doctest
dirty = False
template.enable_color()
for m in [seqdb, iomode, cstr, char, esc, csi, cstr,
          input, output, controller]:
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

