# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from trachet import __version__, __license__, __author__
import inspect, os

filename = inspect.getfile(inspect.currentframe())
dirpath = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))

setup(name                  = 'trachet',
      version               = __version__,
      description           = 'Provides step-by-step debugging and formatted sequence tracing service, with terminal applications.',
      long_description      = open(dirpath + "/README.rst").read(),
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
      url                   = 'https://github.com/saitoha/trachet',
      license               = __license__,
      packages              = find_packages(exclude=[]),
      zip_safe              = True,
      include_package_data  = False,
      install_requires      = ['tff >=0.0.10, <0.1.0'],
      entry_points          = """
                              [console_scripts]
                              trachet = trachet:main
                              """
      )

