#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012-2014  Hayaki Saito <user@zuse.jp>
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

import sys
import os
import logging


# print version and license information
def _printver():
    import __init__

    print '''
trachet %s
Copyright (C) 2012-2014 Hayaki Saito <user@zuse.jp>.

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


def _parse_options():

    import optparse

    # parse options and arguments
    usage = 'usage: %prog [options] command'
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-o', '--output', dest='output',
                      default='trachetscript',
                      help='specify output device or file')

    parser.add_option('-b', '--break', dest='breakstart',
                      action="store_true", default=False,
                      help='"break" the program at the startup time'
                      '  default: false')

    parser.add_option('-m', '--monochrome', dest='monochrome',
                      action="store_true", default=False,
                      help='don\'t use color in output terminal')

    parser.add_option('-v', '--version', dest='version',
                      action="store_true", default=False,
                      help='show version')

    return parser.parse_args()


def _prepare_starting_command(args):
    # retrive starting command
    if len(args) == 1:
        command = args[0]
    elif len(args) > 1:
        command = " ".join(args)
    elif 'SHELL' in os.environ:
        command = os.getenv('SHELL')
    else:
        command = '/bin/sh'
    return command


def _prepare_term():
    # retrive TERM setting
    if 'TERM' in os.environ:
        term = os.getenv('TERM')
    else:
        term = 'xterm'
    return term


def _prepare_lang():
    # retrive LANG setting
    if 'LANG' in os.environ:
        lang = os.getenv('LANG')
    else:
        import locale
        lang = '%s.%s' % locale.getdefaultlocale()
    return lang


def _check_output_device(filename, monochrome):
    import template
    try:
        fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_NONBLOCK)
    except OSError, e:
        logging.exception(e)
        logging.exception("Connection closed.")
        print "Cannot access output file or device.\n(%s)" % filename
        return False

    try:
        if os.isatty(fd):
            if not os.path.exists(filename):
                print "The output device %s is not found." % filename
                return False
            if filename == os.ttyname(0):
                print ("The output device %s is busy (current TTY). "
                       "Please specify another TTY device.") % filename
                return False
            if monochrome:
                template.disable_color()
            else:
                template.enable_color()
        else:
            template.disable_color()
    finally:
        os.close(fd)
    return True


def mainimpl(options, command, term, lang, termenc):
    from tffstub import tff
    import input
    import output
    import controller
    import trace

    if not _check_output_device(options.output, options.monochrome):
        return

    tty = tff.DefaultPTY(term, lang, command, sys.stdin)
    try:
        tty.fitsize()

        controller = controller.ActionController(tty)
        tracer = trace.TraceHandler(options.output,
                                    termenc,
                                    controller)

        if options.breakstart:
            controller.set_break()

        session = tff.Session(tty)
        session.start(stdin=sys.stdin,
                      stdout=sys.stdout,
                      termenc=termenc,
                      inputhandler=input.InputHandler(controller, tracer),
                      outputhandler=output.OutputHandler(controller, tracer))
    except IOError, e:
        logging.exception(e)
        logging.exception("Connection closed.")
        print "Connection closed."
    except Exception, e:
        logging.exception(e)
        logging.exception("Aborted by exception.")
        print 'trachet aborted by an uncaught exception.'
        print ' see $HOME/.trachet/log/log.txt.'
    finally:
        try:
            tty.restore_term()
        except Exception, e:
            logging.exception(e)


def main():
    ''' entry point function for command line program '''
    options, args = _parse_options()

    if options.version:
        _printver()
        return
    command = _prepare_starting_command(args)
    term = _prepare_term()
    lang = _prepare_lang()

    # retrive terminal encoding setting
    import locale
    termenc = locale.getdefaultlocale()[1]

    if not termenc:
        termenc = "UTF-8"

    # fix for cygwin environment, such as utf_8_cjknarrow
    if termenc.lower().startswith("utf_8_"):
        termenc = "UTF-8"

    logdir = os.path.expanduser('~/.trachet/log')
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    logfile = os.path.join(logdir, "log.txt")
    logging.basicConfig(filename=logfile, filemode="w")

    mainimpl(options, command, term, lang, termenc)


# main
if __name__ == '__main__':
    main()
