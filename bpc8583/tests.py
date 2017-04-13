#!/usr/bin/env python

import unittest

from ISO8583 import ISO8583, MemDump
from py8583spec import IsoSpec, IsoSpec1987BPC
from terminal import Terminal
from card import Card
from transaction import Transaction
from isoTools import get_response

class TestTerminal(unittest.TestCase):

    def setUp(self):
        self.term = Terminal()
        self.term.set_terminal_key('deadbeef deadbeef deadbeef deadbeef')

    """
    terminal._get_pinblock()
    """

    def test_get_pinblock_empty_pin(self):
        self.assertEqual(self.term._get_pinblock('', '4000001234562000'), None)

    def test_get_pinblock_empty_pan(self):
        self.assertEqual(self.term._get_pinblock('1234', ''), None)

    def test_get_pinblock_pin_passed_as_int(self):
        self.assertEqual(self.term._get_pinblock(1234, '4000001234562000'), '041274ffffedcba9')

    def test_get_pinblock_cardnumber_passed_as_int(self):
        self.assertEqual(self.term._get_pinblock('1234', 4000001234562000), '041274ffffedcba9')    

    def test_get_pinblock_length_4(self):
        self.assertEqual(self.term._get_pinblock('1234', '4000001234562000'), '041274ffffedcba9')

    def test_get_pinblock_length_5(self):
        self.assertEqual(self.term._get_pinblock('92389', '4000001234562000'), '0592789fffedcba9')

    """
    terminal.get_encrypted_pin()
    """

    def test_get_encrypted_pin(self):
        self.assertEqual(self.term.get_encrypted_pin('1234', '4000001234562000'), '11E7C600A7E2988B')


class TestIsoTools(unittest.TestCase):
    
    """
    get_response()
    """
    def test_get_response_empty_code(self):
        self.assertEqual(get_response(''), None)

    def test_get_response_0100(self):
        self.assertEqual(get_response('0100'), '0110')

    def test_get_response_100(self):
        self.assertEqual(get_response('100'), '110')

    def test_get_response_passed_as_integer(self):
        self.assertEqual(get_response(200), '210')

if __name__ == '__main__':
    unittest.main()