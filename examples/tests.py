#!/usr/bin/env python

import unittest
import binascii
import os

import CBS

class TestCBS(unittest.TestCase):
    
    def setUp(self):
        self.IsoPacket = ISO8583(IsoSpec = IsoSpec1987ASCII())
        self.IsoPacket.Strict(True)
    
    def tearDown(self):
        pass
    
    def test_MTI(self):
        self.assertEqual(self.IsoPacket.MTI(), MTI)

if __name__ == '__main__':
    unittest.main()                        