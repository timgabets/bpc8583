#!/usr/bin/env python

import unittest
import binascii
import os

from CBS import get_message_length, get_balance_string

class TestGetMessageLength(unittest.TestCase):
    
    def test_get_message_length_ascii_empty(self):
        self.assertEqual(get_message_length(b''), b'\x00\x00')
 
    def test_get_message_length_ascii_XX(self):
        self.assertEqual(get_message_length(b'XX'), b'\x00\x02')

    def test_get_message_length_ascii_length_28(self):
        self.assertEqual(get_message_length(b'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'), b'\x00\x28')

    def test_get_message_length_ascii_length_216(self):
        self.assertEqual(get_message_length(b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'), b'\x02\x16')


class TestGetBalanceString(unittest.TestCase):
    def test_get_balance_string_empty(self):
        self.assertEqual(get_balance_string('', ''), '')

    def test_get_balance_string_positive(self):
        self.assertEqual(get_balance_string('1234.56', '643'), '200001643C000000123456')

    def test_get_balance_string_negative(self):
        self.assertEqual(get_balance_string('-1234.59', '826'), '200001826D000000123459')

    def test_get_balance_string_unstripped(self):
        self.assertEqual(get_balance_string('  -1234.59 ', '826'), '200001826D000000123459')

if __name__ == '__main__':
    unittest.main()                        