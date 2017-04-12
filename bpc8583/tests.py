#!/usr/bin/env python

import unittest

from ISO8583 import ISO8583, MemDump
from py8583spec import IsoSpec, IsoSpec1987BPC
from terminal import Terminal
from card import Card
from transaction import Transaction

class TestTerminal(unittest.TestCase):

    def setUp(self):
        self.term = Terminal()

    def test_get_pinblock(self):
        self.assertEqual(self.term.get_pinblock('1234'), 'FOO')

if __name__ == '__main__':
    unittest.main()