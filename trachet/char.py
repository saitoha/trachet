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

import seqdb
import template

_DB = seqdb.get()

_CHAR_MAP = {0x00: '<NUL>',
             0x01: '<SOH>',
             0x02: '<STX>',
             0x03: '<ETX>',
             0x04: '<EOT>',
             0x05: '<ENQ>',
             0x06: '<ACK>',
             0x07: '<BEL>',
             0x08: '<BS>',
             0x09: '<HT>',
             0x0A: '<NL>',
             0x0B: '<VT>',
             0x0C: '<NP>',
             0x0D: '<CR>',
             0x0E: '<SO>',
             0x0F: '<SI>',
             0x10: '<DLE>',
             0x11: '<DC1>',
             0x12: '<DC2>',
             0x13: '<DC3>',
             0x14: '<DC4>',
             0x15: '<NAK>',
             0x16: '<SYN>',
             0x17: '<ETB>',
             0x18: '<CAN>',
             0x19: '<EM>',
             0x1A: '<SUB>',
             0x1B: '<ESC>',
             0x1C: '<FS>',
             0x1D: '<GS>',
             0x1E: '<RS>',
             0x1F: '<US>',
             0x20: '<SP>',
             0x7F: '<DEL>'}


def get_mnemonic(key):
    """
      >>> _create_mock_db()
      >>> get_mnemonic('< <BEL>')
      'BEL / Ctrl-G'
      >>> get_mnemonic('< <DEL>')
      ''
    """
    if key in _DB:
        return _DB[key]
    return ""


def format(c, is_input, tracer, controller):
    """
      >>> _create_mock_db()
      >>> str(format(ord("a"), False, None, None)).replace("\x1b", "\\x1b")
      "(u'\\\\x1b[32ma\\\\x1b[m', False)"
      >>> str(format(ord("\x1b"), False, None, None)).replace("\x1b", "\\x1b")
      "('\\\\x1b[32m<ESC>\\\\x1b[m', False)"
      >>> str(format(ord("\x07"), False, None, None)).replace("\x1b", "\\x1b")
      "('\\\\x1b[31m<BEL>\\\\x1b[1;32m\\\\r\\\\x1b[30CBEL / bell\\\\x1b[m', True)"
    """

    if c in _CHAR_MAP:
        printable_char = _CHAR_MAP[c]
    else:
        try:
            printable_char = unichr(c)
        except:
            c1 = (c >> 10) + 0xd800
            c2 = (c & 0x3ff) + 0xdc00
            printable_char = unichr(c1) + unichr(c2)

    if is_input:
        direction = '<'
    else:
        direction = '>'

    key = "%s %s" % (direction, printable_char)

    mnemonic = get_mnemonic(key)
    if mnemonic:
        if mnemonic[0] == "!":
            return eval(mnemonic[1:])
        return template.getprintablechar() % (printable_char, mnemonic), True
    return template.getchar() % printable_char, False


def _create_mock_db():
    global _DB
    _DB = {
        '< <NUL>': 'NUL / Ctrl-@,Ctrl-SP,Ctrl-2',
        '< <BEL>': 'BEL / Ctrl-G',
        '> <NUL>': 'NUL / null character',
        '> <BEL>': 'BEL / bell',
    }


if __name__ == "__main__":
    import doctest
    doctest.testmod()
