#!/usr/bin/env python

import unittest
import binascii
import os

from bpc8583.card import Card
from bpc8583.terminal import Terminal
from bpc8583.transaction import Transaction
from bpc8583.tools import get_response, get_random_hex
from bpc8583.ISO8583 import ISO8583, ParseError, Bcd2Str, Str2Bcd
from bpc8583.spec import IsoSpec1987ASCII, IsoSpec1987BCD


class TestBcd2Str(unittest.TestCase):
    def test_bcd2str_empty(self):
        self.assertEqual(Bcd2Str(b''), '')

    def test_bcd2str_00fa(self):
        self.assertEqual(Bcd2Str(b'00fa'), '30306661')


class TestStr2Bcd(unittest.TestCase):
    def test_str2bcd_empty(self):
        self.assertEqual(Str2Bcd(''), b'')

    def test_str2bcd_00fa(self):
        self.assertEqual(Str2Bcd('00fa'), b'\x00\xfa')

    def test_str2bcd_99b(self):
        self.assertEqual(Str2Bcd('55b'), b'\x05\x5b')


class TestAsciiParse1987(unittest.TestCase):
    
    def setUp(self):
        self.IsoPacket = ISO8583(IsoSpec = IsoSpec1987ASCII())
        self.IsoPacket.Strict(True)
    
    def tearDown(self):
        pass
    
    def test_description_field_2(self):
        self.assertEqual(self.IsoPacket.Description(2), 'Primary account number (PAN)')

    def test_description_non_existent_field(self):
        self.assertEqual(self.IsoPacket.Description(200), '')    

    def test_MTI(self):
        # positive test
        for b1 in range(0, 9):
            for b2 in range(1, 9):
                for b3 in range(0,9):
                    for b4 in range(0, 5):
                        MTI = str(b1) + str(b2) + str(b3) + str(b4)
                        self.IsoPacket.SetIsoContent((MTI + "0000000000000000").encode('latin'))
                        self.assertEqual(self.IsoPacket.MTI(), MTI)
    
        # negative test
        with self.assertRaisesRegex(ParseError, "Invalid MTI"):
            self.IsoPacket.SetIsoContent("000A".encode('latin'))
            
        with self.assertRaisesRegex(ParseError, "Invalid MTI"):
            self.IsoPacket.SetIsoContent("0000".encode('latin'))
            
        for b4 in range(6, 9):
            with self.assertRaisesRegex(ParseError, "Invalid MTI"):
                MTI = "010" + str(b4)
                self.IsoPacket.SetIsoContent(MTI.encode('latin'))
                
    def test_Bitmap(self):
        
        # Primary bitmap
        for shift in range(0, 63):
            bitmap = '{:0>16X}'.format(1 << shift)
            content = '0200' +  bitmap + ''.zfill(256)

            self.IsoPacket.SetIsoContent(content.encode('latin'))
            self.assertEqual(self.IsoPacket.Bitmap()[64 - shift], 1)
            self.assertEqual(self.IsoPacket.Field(64 - shift), 1)
            
        # Secondary bitmap
        for shift in range(0, 64):
            bitmap = '8{:0>31X}'.format(1 << shift)
            content = '0200' +  bitmap + ''.zfill(256)
            
            self.IsoPacket.SetIsoContent(content.encode('latin'))
            self.assertEqual(self.IsoPacket.Bitmap()[128 - shift], 1)
            self.assertEqual(self.IsoPacket.Field(128 - shift), 1)

    """
    RemoveField()
    """
    def test_remove_field(self):
        self.IsoPacket.FieldData(39, '00')
        self.IsoPacket.FieldData(4, '000000000000')
        self.assertEqual(self.IsoPacket.Bitmap(), {4:1, 39: 1})
        self.assertEqual(self.IsoPacket.FieldData(39), '00')

        self.IsoPacket.RemoveField(39)
        self.assertEqual(self.IsoPacket.Bitmap(), {4: 1})
        self.assertEqual(self.IsoPacket.FieldData(39), None)


    def test_remove_non_existent_field(self):
        self.assertEqual(self.IsoPacket.Bitmap(), {})
        self.IsoPacket.RemoveField(39)
        self.assertTrue(True)

                
class TestBCDParse1987(unittest.TestCase):
    
    def setUp(self):
        self.IsoPacket = ISO8583(IsoSpec = IsoSpec1987BCD())
        self.IsoPacket.Strict(True)
    
    def tearDown(self):
        pass
    
    def test_MTI(self):
        # positive test
        for b1 in range(0, 9):
            for b2 in range(1, 9):
                for b3 in range(0,9):
                    for b4 in range(0, 5):                        
                        MTI = str(b1) + str(b2) + str(b3) + str(b4)
                        self.IsoPacket.SetIsoContent(binascii.unhexlify(MTI + "0000000000000000"))
                        self.assertEqual(self.IsoPacket.MTI(), MTI)
                        
        # negative test
        with self.assertRaisesRegex(ParseError, "Invalid MTI"):
            self.IsoPacket.SetIsoContent(binascii.unhexlify("000A"))

        with self.assertRaisesRegex(ParseError, "Invalid MTI"):
            self.IsoPacket.SetIsoContent(binascii.unhexlify("0000"))
            
        for b4 in range(6, 9):
            with self.assertRaisesRegex(ParseError, "Invalid MTI"):
                MTI = binascii.unhexlify("010" + str(b4))
                self.IsoPacket.SetIsoContent(MTI)


class TestTerminal(unittest.TestCase):

    def setUp(self):
        self.default_terminal_key = 'DEADBEEFDEADBEEFDEADBEEFDEADBEEF'
        self.term = Terminal(terminal_key=self.default_terminal_key, show_keys=False)

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
        self.assertEqual(self.term.get_encrypted_pin('1234', '4000001234562000'), 'C3BA1E04D88654C4')

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

    """
    terminal.get_country_code()
    """
    def test_get_country_code(self):
        self.assertEqual(self.term.get_country_code(), '0643')


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

    def test_get_response_auth_advice_1120(self):
        self.assertEqual(get_response('1120'), '1130')

    def test_get_response_network_mgmt_0800(self):
        self.assertEqual(get_response('0800'), '0810')

    """
    get_random_hex()
    """
    def test_get_random_hex_0_length(self):
        self.assertEqual(get_random_hex(0), '')

    def test_get_random_hex_2(self):
        self.assertEqual(len(get_random_hex(2)), 2)

    def test_get_random_hex_5(self):
        self.assertEqual(len(get_random_hex(5)), 5)

    def test_get_random_hex_16(self):
        self.assertEqual(len(get_random_hex(16)), 16)


class TestTransactionClass(unittest.TestCase):

    def setUp(self):
        self.term = Terminal(show_keys=False)
        self.card = Card()
        self.trxn = Transaction('echo', self.card, self.term)
        self.trxn.set_description('Test echo')

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

    """
    trxn.get_description()
    """
    def test_trxn_description_card_description_empty(self):
        self.assertEqual(self.trxn.get_description(), 'Test echo')

    def test_trxn_description_card_description_not_empty(self):
        card_description = 'On-us card 445566'
        self.card.set_description(card_description)
        self.assertEqual(self.trxn.get_description(), card_description + ' | Test echo')

    """
    trxn.set_currency()
    """
    def test_trxn_set_valid_currency(self):
        self.trxn.set_currency('USD')
        self.assertEqual(self.trxn.get_currency(), 840)

    def test_trxn_set_invalid_currency(self):
        self.trxn.set_currency('IDDQD')
        self.assertIsNone(self.trxn.get_currency())

class TestTerminalKeyStorage(unittest.TestCase):
    
    def setUp(self):
        self.term = Terminal(show_keys=False)
        self.key = 'C3BA1E04D88654C4'
        self.keyfile = '.terminalkey.cache'
        self._remove_keyfile()

    def tearDown(self):
        self._remove_keyfile()

    def _remove_keyfile(self):
        try:
            os.remove(self.keyfile)
        except FileNotFoundError:
            pass

    def test_terminal_key_stored(self):
        self.assertTrue(self.term.store_terminal_key(self.key))
        self.assertEqual(self.term.get_stored_key(), self.key)
        


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

    def test_get_service_code(self):
        self.assertEqual(self.card.get_service_code(), '101')

    def test_get_expiry_date(self):
        self.assertEqual(self.card.get_expiry_date(), 1120)

    def test_get_card_number(self):
        self.assertEqual(self.card.get_card_number(), 4444555566667777)

    def test_get_transaction_counter_length_1(self):
        self.card._set_transaction_counter(1)
        self.assertEqual(self.card.get_transaction_counter(), '0001')        

    def test_get_transaction_counter_length_2(self):
        self.card._set_transaction_counter(88)
        self.assertEqual(self.card.get_transaction_counter(), '0088') 

    def test_get_transaction_counter_length_3(self):
        self.card._set_transaction_counter(777)
        self.assertEqual(self.card.get_transaction_counter(), '0777') 

    def test_get_transaction_counter_length_4(self):
        self.card._set_transaction_counter(9999)
        self.assertEqual(self.card.get_transaction_counter(), '9999') 

if __name__ == '__main__':
    unittest.main()