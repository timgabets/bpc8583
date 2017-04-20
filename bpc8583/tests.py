#!/usr/bin/env python

import unittest

from ISO8583 import ISO8583, MemDump
from py8583spec import IsoSpec, IsoSpec1987BPC
from terminal import Terminal
from card import Card
from transaction import Transaction
from isoTools import get_response, dump

class TestTerminal(unittest.TestCase):

    def setUp(self):
        self.default_terminal_key = 'DEADBEEFDEADBEEFDEADBEEFDEADBEEF'
        self.term = Terminal(key=self.default_terminal_key)

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
    def test_get_encrypted_pin_empty_pin_empty_cardnumber(self):
        self.assertEqual(self.term.get_encrypted_pin('', ''), '')

    def test_get_encrypted_pin_invalid_pin(self):
        self.assertEqual(self.term.get_encrypted_pin('iddqd', '4000001234562000'), '')

    def test_get_encrypted_pin_invalid_cardnumber(self):
        self.assertEqual(self.term.get_encrypted_pin('1234', 'iddqd'), '')

    def test_get_encrypted_pin_valid_digits(self):
        self.assertEqual(self.term.get_encrypted_pin('1234', '4000001234562000'), '11E7C600A7E2988B')

    """
    terminal.get_terminal_key()
    """
    def test_get_default_terminal_key(self):
        self.assertEqual(self.term.get_terminal_key(), self.default_terminal_key)

    
    """
    terminal.set_terminal_key()
    """
    def test_set_new_empty_terminal_key(self):        
        self.assertFalse(self.term.set_terminal_key(''))

    def test_set_new_terminal_key_with_invalid_characters(self):  
        self.assertFalse(self.term.set_terminal_key('invalid key'))

    def test_set_new_terminal_key_with_invalid_length_key(self):  
        self.assertFalse(self.term.set_terminal_key('DEAFBEEDEAFBEE'))

    def test_set_new_terminal_key(self):
        new_key_value = '00001111222233334444555566667777'
        self.assertTrue(self.term.set_terminal_key(new_key_value))
        self.assertEqual(self.term.get_terminal_key(), new_key_value) 


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

    """
    dump()
    """
    def test_dump_short_message(self):
        self.assertEqual(dump(b'iddqd'), '\t69 64 64 71 64                                          iddqd\n\t')

    def test_dump_one_line_ascii(self):
        self.assertEqual(dump(b'testdatatestdata'), '\t74 65 73 74 64 61 74 61 74 65 73 74 64 61 74 61         testdatatestdata\n\t')

    def test_dump_one_line_non_ascii(self):
        self.assertEqual(dump(b'\x11\x12\x13\x14datatestdata'), '\t11 12 13 14 64 61 74 61 74 65 73 74 64 61 74 61         ....datatestdata\n\t')

    def test_dump_two_lines_ascii(self):
        self.assertEqual(dump(b'loremipsumdolorsitamet'), '\t6c 6f 72 65 6d 69 70 73 75 6d 64 6f 6c 6f 72 73         loremipsumdolors\n\t69 74 61 6d 65 74                                       itamet\n\t')


class TestTransactionClass(unittest.TestCase):

    def setUp(self):
        self.term = Terminal()
        self.card = Card()
        self.trxn = Transaction('echo', self.card, self.term)


    """
    trxn.set_expected_action()
    """
    def test_set_expected_action_approve(self):
        self.assertEqual(self.trxn.set_expected_action('approve'), True)
        self.assertEqual(self.trxn.expected_response_action, 'APPROVE')

    def test_set_expected_action_decline(self):
        self.assertEqual(self.trxn.set_expected_action('decline'), True)
        self.assertEqual(self.trxn.expected_response_action, 'DECLINE')

    def test_set_expected_action_mixed_case(self):
        self.assertEqual(self.trxn.set_expected_action('ApPrOVe'), True)
        self.assertEqual(self.trxn.expected_response_action, 'APPROVE')

    def test_set_expected_action_empty(self):
        self.assertEqual(self.trxn.set_expected_action(''), False)
        self.assertEqual(self.trxn.expected_response_action, None)

    def test_set_expected_action_unknown(self):
        self.assertEqual(self.trxn.set_expected_action('no reason to decline'), False)
        self.assertEqual(self.trxn.expected_response_action, None)

    """
    trxn.is_response_expected()
    """
    def test_is_response_expected_resp_codes_resp_action_are_not_set(self):
        self.assertEqual(self.trxn.is_response_expected('000'), True)

    def test_is_response_expected_resp_codes_equal(self):
        self.trxn.set_expected_code('000')
        self.assertEqual(self.trxn.is_response_expected('000'), True)

    def test_is_response_expected_resp_codes_not_equal(self):
        self.trxn.set_expected_code('999')
        self.assertEqual(self.trxn.is_response_expected('000'), False)

    def test_is_response_expected_resp_action_APPROVED_resp_code_000(self):
        self.trxn.set_expected_action('APPROVED')
        self.assertEqual(self.trxn.is_response_expected('000'), True)

    def test_is_response_expected_resp_action_APPROVED_resp_code_999(self):
        self.trxn.set_expected_action('APPROVED')
        self.assertEqual(self.trxn.is_response_expected('999'), False)

    def test_is_response_expected_resp_action_DECLINED_resp_code_000(self):
        self.trxn.set_expected_action('DECLINED')
        self.assertEqual(self.trxn.is_response_expected('000'), False)

    def test_is_response_expected_resp_action_DECLINED_resp_code_999(self):
        self.trxn.set_expected_action('DECLINED')
        self.assertEqual(self.trxn.is_response_expected('777'), True)


class TestCardClass(unittest.TestCase):

    def setUp(self):
        self.pan = '4444555566667777'
        self.expiry_date = '1120'
        self.service_code = '101'
        self.PVV_key_index = 1
        self.PVV = '8723'
        self.CVV = '000'
        self.discretionary_data = '00720'

        self.card = Card(pan=self.pan, 
            expiry_date=self.expiry_date, 
            service_code=self.service_code, 
            pvvki=self.PVV_key_index,
            PVV=self.PVV,
            CVV=self.CVV,
            discretionary_data=self.discretionary_data)

    def test_get_track2(self):
        self.assertEqual(self.card.get_track2(), '4444555566667777=11201011872300000720')

    def test_get_expiry_date(self):
        self.assertEqual(self.card.get_expiry_date(), 1120)

    def test_get_card_number(self):
        self.assertEqual(self.card.get_card_number(), 4444555566667777)        

if __name__ == '__main__':
    unittest.main()