#!/usr/bin/env python
# -*- coding:utf-8
import unittest
import doctest


class DocTest(unittest.TestCase):

    def test_tff(self):
        import trachet.tffstub as tffstub
        from trachet.tffstub import tff
        print tffstub.expected_hash
        print tff.signature
        print tff.__version__
        #self.assertTrue(tffstub.expected_hash == tff.signature)

    def test_templete(self):
        import trachet.template as template
        template.enable_color()
        failure_count, test_count = doctest.testmod(template)
        self.assertTrue(failure_count == 0)

    def test_seqdb(self):
        import trachet.template as template
        import trachet.seqdb as seqdb
        template.enable_color()
        failure_count, test_count = doctest.testmod(seqdb)
        self.assertTrue(failure_count == 0)

    def test_iomode(self):
        import trachet.template as template
        import trachet.iomode as iomode
        template.enable_color()
        failure_count, test_count = doctest.testmod(iomode)
        self.assertTrue(failure_count == 0)

    def test_char(self):
        import trachet.template as template
        import trachet.char as char
        template.enable_color()
        failure_count, test_count = doctest.testmod(char)
        self.assertTrue(failure_count == 0)

    def test_esc(self):
        import trachet.template as template
        import trachet.esc as esc
        template.enable_color()
        failure_count, test_count = doctest.testmod(esc)
        self.assertTrue(failure_count == 0)

    def test_csi(self):
        import trachet.template as template
        import trachet.csi as csi
        template.enable_color()
        failure_count, test_count = doctest.testmod(csi)
        self.assertTrue(failure_count == 0)

    def test_cstr(self):
        import trachet.template as template
        import trachet.cstr as cstr
        template.enable_color()
        failure_count, test_count = doctest.testmod(cstr)
        self.assertTrue(failure_count == 0)

    def test_input(self):
        import trachet.template as template
        import trachet.input as input
        template.enable_color()
        failure_count, test_count = doctest.testmod(input)
        self.assertTrue(failure_count == 0)

    def test_output(self):
        import trachet.template as template
        import trachet.output as output
        template.enable_color()
        failure_count, test_count = doctest.testmod(output)
        self.assertTrue(failure_count == 0)

    def test_trace(self):
        import trachet.template as template
        import trachet.trace as trace
        template.enable_color()
        failure_count, test_count = doctest.testmod(trace)
        self.assertTrue(failure_count == 0)

    def test_controller(self):
        import trachet.template as template
        import trachet.controller as controller
        template.enable_color()
        failure_count, test_count = doctest.testmod(controller)
        self.assertTrue(failure_count == 0)

    def test_ss2(self):
        import trachet.template as template
        import trachet.ss2 as ss2
        template.enable_color()
        failure_count, test_count = doctest.testmod(ss2)
        self.assertTrue(failure_count == 0)

    def test_ss3(self):
        import trachet.template as template
        import trachet.ss3 as ss3
        template.enable_color()
        failure_count, test_count = doctest.testmod(ss3)
        self.assertTrue(failure_count == 0)

    def test_constant(self):
        import trachet.template as template
        import trachet.constant as constant
        template.enable_color()
        failure_count, test_count = doctest.testmod(constant)
        self.assertTrue(failure_count == 0)

    def suite():
        suite = unittest.TestSuite()
        suite.addTests(unittest.makeSuite(DocTest))
        return suite
