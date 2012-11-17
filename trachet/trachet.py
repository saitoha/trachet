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

def main():
    import sys, os, optparse, select

    # parse options and arguments
    usage = 'usage: %prog [options] command'
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-o', '--output', dest='output',
                      default='/dev/null',
                      help='OutputFile')

    parser.add_option('--version', dest='version',
                      action="store_true", default=False,
                      help='show version')

    (options, args) = parser.parse_args()

    if options.version:
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
    import codecs

    _TRACE_MODE_NONE        = 0
    _TRACE_MODE_NORMAL_STEP = 1
    _TRACE_MODE_FUZZY_STEP  = 2
    _TRACE_MODE_STOP        = 3

    _TRACE_TYPE_CSI  = 0
    _TRACE_TYPE_ESC  = 1
    _TRACE_TYPE_STR  = 2
    _TRACE_TYPE_CHAR = 3

    class ActionController():

        __mode = _TRACE_MODE_NONE
        __actions = None

        def __init__(self, tty):
            self.__mode = _TRACE_MODE_NONE
            self.__actions = []
            self.__tty = tty

        def append(self, action):
            return self.__actions.append(action)

        def clear(self):
            self.__mode = _TRACE_MODE_NONE
            #self.__tty.xon()

        def is_suspend(self):
            return self.__mode != _TRACE_MODE_NONE

        def set_normal_step(self):
            self.__mode = _TRACE_MODE_NORMAL_STEP

        def set_fuzzy_step(self):
            self.__mode = _TRACE_MODE_FUZZY_STEP

        def set_stop(self):
            self.__mode = _TRACE_MODE_STOP
            #self.__tty.xoff()

        def tick(self):
            if self.__mode == _TRACE_MODE_NONE:
                while len(self.__actions) > 0:
                    action = self.__actions.pop(0)    
                    result = action()
            elif self.__mode == _TRACE_MODE_NORMAL_STEP:
                while len(self.__actions) > 0:
                    action = self.__actions.pop(0)    
                    result = action()
                    if result != _TRACE_TYPE_CHAR:
                        break
                self.__mode = _TRACE_MODE_STOP
            elif self.__mode == _TRACE_MODE_FUZZY_STEP:
                if len(self.__actions) > 0:
                    action = self.__actions.pop(0)    
                    result = action()
                self.__mode = _TRACE_MODE_STOP

    class InputHandler(tff.DefaultHandler):

        def __init__(self, actions, output_file):
            if isinstance(output_file, str):
                output_file = open(output_file, "w")
            self.__output = TraceHandler(output_file)
            self.__log = codecs.getwriter(termenc)(output_file)
            self.__actions = actions

        def handle_csi(self, context, parameter, intermediate, final):
            if final == 0x7e and intermediate == [] and parameter == [0x31, 0x35]:   # F5
                self.__actions.clear()
            if final == 0x7e and intermediate == [] and parameter == [0x31, 0x37]:   # F6
                self.__actions.set_stop()
            elif self.__actions.is_suspend() and final == 0x7e and intermediate == [] and parameter == [0x31, 0x38]: # F7
                self.__actions.set_fuzzy_step()
            elif self.__actions.is_suspend() and final == 0x7e and intermediate == [] and parameter == [0x31, 0x39]: # F8
                self.__actions.set_normal_step()
            else:
                context.write(0x1b)
                context.write(0x5b)
                for c in parameter:
                    context.write(c)
                for c in intermediate:
                    context.write(c)
                context.write(final)
                self.__output.handle_csi(context, parameter, intermediate, final)
            return True 

        def handle_esc(self, context, intermediate, final):
            context.write(0x1b)
            for c in intermediate:
                context.write(c)
            context.write(final)
            self.__output.handle_esc(context, intermediate, final)
            return True 

        def handle_control_string(self, context, prefix, value):
            context.write(0x1b)
            context.write(prefix)
            for c in value:
                context.write(c)
            return True 

        def handle_char(self, context, final):
            if final < 0x100:
                context.write(final)
            else:
                context.writestring(unichr(final))
            self.__output.handle_char(context, final)
            self.__log.write(u"\n\x1b[41m%c\x1b[m\n" % final)
            return True 

        def handle_draw(self, context):
            self.__actions.tick()

    class OutputHandler(tff.DefaultHandler):

        def __init__(self, actions, output_file):
            self.__super = super(tff.DefaultHandler, self)
            self.__output = TraceHandler(output_file)
            self.__super.__init__()
            self.__actions = actions

        def handle_csi(self, context, parameter, intermediate, final):
            def action():
                context.write(0x1b)
                context.write(0x5b)
                for c in parameter:
                    context.write(c)
                for c in intermediate:
                    context.write(c)
                context.write(final)
                self.__output.handle_csi(context, parameter, intermediate, final)
                return _TRACE_TYPE_CSI 
            self.__actions.append(action)
            return True 

        def handle_esc(self, context, intermediate, final):
            def action():
                context.write(0x1b)
                for c in intermediate:
                    context.write(c)
                context.write(final)
                self.__output.handle_esc(context, intermediate, final)
                return _TRACE_TYPE_ESC 
            self.__actions.append(action)
            return True 

        def handle_control_string(self, context, prefix, value):
            def action():
                context.write(0x1b)
                context.write(prefix)
                for c in value:
                    context.write(c)
                return _TRACE_TYPE_STR 
            self.__actions.append(action)
            return True 

        def handle_char(self, context, final):
            def action():
                context.write(final)
                self.__output.handle_char(context, final)
                return _TRACE_TYPE_CHAR 
            self.__actions.append(action)
            return True 

        def handle_draw(self, context):
            self.__actions.tick()

    class TraceHandler(tff.DefaultHandler):

        def __init__(self, output_file):
            if isinstance(output_file, str):
                output_file = open(output_file, "w")
            self.__super = super(TraceHandler, self)
            self.__log = output_file 
            self.__bufferring = False 

        def handle_csi(self, context, parameter, intermediate, final):
            p = ''.join([chr(c) for c in parameter])
            i = ''.join([chr(c) for c in intermediate])
            f = chr(final)
            if self.__bufferring:
                self.__bufferring = False
            if i == '':
                if final == 0x6d: # m
                    mnemonic = 'SGR'
                elif final == 0x4a: # J
                    mnemonic = 'ED'
                elif final == 0x4b: # K
                    mnemonic = 'EL'
                elif final == 0x48: # H
                    mnemonic = 'CUP'
                elif final == 0x64: # d
                    mnemonic = 'VPA'
                elif final == 0x72: # r
                    mnemonic = 'DECSTBM'
                elif final == 0x58: # X
                    mnemonic = 'ECH'
                elif final == 0x54: # T
                    mnemonic = 'SD'
                elif final == 0x68: # h
                    if parameter[0] == 0x3f: #
                        mnemonic = 'DECSET'
                    else:
                        mnemonic = 'SM'
                elif final == 0x6c: # l
                    if parameter[0] == 0x3f: #
                        mnemonic = 'DECRST'
                    else:
                        mnemonic = 'RM'
                else:
                    mnemonic = '[CSI ' + chr(final) + ']'
            else:
                mnemonic = '[CSI ' + i + ':' + chr(final) + ']'

            self.__log.write("\n<\x1b[31m%s \x1b[32m%s\x1b[m>" % (mnemonic, p))
            self.__log.flush()
            return False # not handled

        def handle_esc(self, context, prefix, final):
            mnemonic = '[ESC ' + ''.join([chr(c) for c in prefix]) + ']'
            self.__log.write("\n<\x1b[31m%s \x1b[32m%s\x1b[m>" % (mnemonic, chr(final)))
            return False # not handled

        def handle_control_string(self, context, prefix, value):
            v = ''.join([chr(c) for c in value])
            mnemonic = '[ESC ' + chr(prefix) + ']'
            self.__log.write("\n<\x1b[31m%s \x1b[32m%s\x1b[m>" % (mnemonic, v))
            return False # not handled

        def handle_char(self, context, c):
            try:
                if c < 0x20:
                    mnemonic = ['NUL', 'SOH', 'STX', 'ETX',
                                'EOT', 'ENQ', 'ACK', 'BEL',
                                'BS',  'HT',  'NL',  'VT',
                                'NP',  'CR',  'SO',  'SI', 
                                'DLE', 'DC1', 'DC2', 'DC3',
                                'DC4', 'NAK', 'SYN', 'ETB',
                                'CAN', 'EM',  'SUB', 'ESC',
                                'FS',  'GS',  'RS',  'US',
                                'SP'][c]
                    self.__log.write("\n<\x1b[33m%s\x1b[m>" % mnemonic)
                    self.__bufferring = False
                else:
                    if not self.__bufferring:
                        self.__log.write('\n')
                    self.__log.write(unichr(c).encode(termenc))
                    self.__bufferring = True
                self.__log.flush()
            except:
                pass
            return False # not handled


    tty = tff.DefaultPTY(term, lang, command, sys.stdin)
    tty.fitsize()

    session = tff.Session(tty)
    controller = ActionController(tty) 
    session.start(stdin=sys.stdin,
                  stdout=sys.stdout,
                  termenc=termenc,
                  inputhandler=InputHandler(controller, options.output),
                  outputhandler=OutputHandler(controller, options.output))

''' main '''
if __name__ == '__main__':    
    main()

