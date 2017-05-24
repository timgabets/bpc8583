#!/usr/bin/env python

import unittest
import binascii
import os

from CBS import get_message_length 

class TestGetMessageLength(unittest.TestCase):
    
    def test_get_message_length_ascii_empty(self):
        self.assertEqual(get_message_length(b''), b'\x00\x00')
 
    def test_get_message_length_ascii_XX(self):
        self.assertEqual(get_message_length(b'XX'), b'\x00\x02')

    def test_get_message_length_ascii_length_28(self):
        self.assertEqual(get_message_length(b'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'), b'\x00\x28')

    def test_get_message_length_ascii_length_216(self):
        self.assertEqual(get_message_length(b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'), b'\x02\x16')

if __name__ == '__main__':
    unittest.main()                        