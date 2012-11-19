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

def _printver():
        import __init__
        print '''
trachet %s
Copyright (C) 2012 Hayaki Saito <user@zuse.jp>. 

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
        ''' % __init__.__version__
        return


def main():
    import sys, os, optparse, select

    # parse options and arguments
    usage = 'usage: %prog [options] command'
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-o', '--output', dest='output',
                      default='/dev/null',
                      help='OutputFile')

    parser.add_option('-b', '--break', dest='breakstart',
                      action="store_true", default=False,
                      help='"break" the program at the startup time')

    parser.add_option('--version', dest='version',
                      action="store_true", default=False,
                      help='show version')

    (options, args) = parser.parse_args()

    if options.version:
        _printver()
        return

    # retrive starting command
    if len(args) > 0:
        command = args[0]
    elif not os.getenv('SHELL') is None:
        command = os.getenv('SHELL')
    else:
        command = '/bin/sh'

    # retrive TERM setting
    if not os.getenv('TERM') is None:
        term = os.getenv('TERM')
    else:
        term = 'xterm'

    # retrive LANG setting
    if not os.getenv('LANG') is None:
        lang = os.getenv('LANG')
    else:
        import locale
        lang = '%s.%s' % locale.getdefaultlocale()

    # retrive terminal encoding setting
    import locale
    language, encoding = locale.getdefaultlocale()
    termenc = encoding

    import tff
    import input
    import output
    import controller
    import trace

    tty = tff.DefaultPTY(term, lang, command, sys.stdin)
    tty.fitsize()


    controller = controller.ActionController(tty) 
    tracer = trace.TraceHandler(options.output, termenc)

    if options.breakstart:
        controller.set_break()

    session = tff.Session(tty)
    session.start(stdin=sys.stdin,
                  stdout=sys.stdout,
                  termenc=termenc,
                  inputhandler=input.InputHandler(controller, tracer),
                  outputhandler=output.OutputHandler(controller, tracer))

''' main '''
if __name__ == '__main__':    
    main()

