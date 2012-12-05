# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from trachet import __version__, __license__, __author__
import inspect, os

filename = inspect.getfile(inspect.currentframe())
dirpath = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))

try:
    import trachet.tff
except:
    print "Please do:\n git submodule update --init"
    import sys
    sys.exit(1)

import trachet.seqdb as seqdb
import trachet.iomode as iomode
import trachet.char as char
import trachet.esc as esc
import trachet.csi as csi
import trachet.cstr as cstr
#import trachet.input as input
#import trachet.output as output
#import trachet.trace as trace
#import trachet.controller as controller

import doctest
dirty = False
for m in [seqdb, iomode, cstr, char, esc, csi, cstr]:
    failure_count, test_count = doctest.testmod(m)
    if failure_count > 0:
        dirty = True
if dirty:
    raise Exception("test failed.")

setup(name                  = 'trachet',
      version               = __version__,
      description           = 'Provides step-by-step debugging and formatted sequence tracing service, with terminal applications.',
      long_description      = open(dirpath + "/README.rst").read(),
      py_modules            = ['trachet', 'tff'],
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
      url                   = 'https://github.com/saitoha/trachet',
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

