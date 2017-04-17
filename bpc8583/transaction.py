import struct

from ISO8583 import ISO8583
from isoTools import trace, get_datetime_with_year, get_datetime, get_stan
from py8583spec import IsoSpec, IsoSpec1987BPC
from datetime import datetime

class Transaction():
    def __init__(self, type, card, term):
        """
        """
        self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
        self.card = card
        self.term = term
        self.type = type.lower()
        self.description = ''
        self.expected_response_code = '000'
        self.expected_response_action = None

        if self.type == 'echo':
            """
            """
            self.IsoMessage.MTI("0800")

            self.IsoMessage.FieldData(3, 990000)
            self.IsoMessage.FieldData(12, get_datetime_with_year())


        elif self.type == 'balance':
            """
            """
            self.IsoMessage.MTI("0100")
            
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(3, 310000)
            self.IsoMessage.FieldData(4, 0)
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(13, 1216)
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        elif self.type == 'purchase':
            """
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())            
            self.IsoMessage.MTI("0200")
        
            self.IsoMessage.FieldData(2, self.card.get_card_number())
            self.IsoMessage.FieldData(3, 000000)
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, self.term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, self.card.get_track2())

        else:
            print('Unknown transaction type: {}'.format(_type))
            return None
    
        # Common message fields:
        self.IsoMessage.FieldData(7, get_datetime())
        self.IsoMessage.FieldData(11, get_stan())
        self.IsoMessage.FieldData(41, self.term.get_terminal_id())
        self.IsoMessage.FieldData(42, self.term.get_merchant_id())
        self.IsoMessage.FieldData(49, self.term.get_currency_code())

        self.rebuild()


    def get_data(self):
        """
        """
        return struct.pack("!H", len(self.data)) + self.data


    def rebuild(self):
        """
        Rebuild IsoMessage (e.g. after field data change)
        """
        self.data = self.IsoMessage.BuildIso()


    def trace(self, header=None):
        """
        """
        self.IsoMessage.Print(header=header)


    def set_description(self, description):
        """
        """
        self.description = description


    def get_description(self):
        """
        Get transaction description (for logging purposes)
        """
        if self.description:
            return self.description
        else:
            return self.type + ' ' + str(self.IsoMessage.FieldData(11))


    def set_PIN(self, PIN):
        """
        """
        if PIN:
            encrypted_pinblock = self.term.get_encrypted_pin(PIN, self.card.get_card_number())
            if encrypted_pinblock:
                self.IsoMessage.FieldData(52, encrypted_pinblock)
                self.rebuild()


    def set_amount(self, amount):
        """
        Set transaction amount
        """
        if amount:
            try:
                self.IsoMessage.FieldData(4, int(amount))
            except ValueError:
                self.IsoMessage.FieldData(4, 0)
            self.rebuild()


    def set_expected_code(self, expected_response_code):
        """
        Expected response code of the transaction
        """
        self.expected_response_code = expected_response_code


    def set_expected_action(self, expected_response_action):
        """
        Expected outcome of the transaction ('APPROVED' or 'DECLINED')
        """
        if expected_response_action.upper() not in ['APPROVED', 'APPROVE', 'DECLINED', 'DECLINE']:
            return False

        self.expected_response_action = expected_response_action.upper()
        return True


    def is_response_expected(self, actual_response_code):
        """
        """
        if self.expected_response_action in ['APPROVED', 'APPROVE']:
            if int(actual_response_code) == 0:
                return True
            else:
                return False

        elif self.expected_response_action in ['DECLINED', 'DECLINE']:
            if int(actual_response_code) != 0:
                return True
            else:
                return False
        else:
            # no response action available, compare the response codes:
            if self.expected_response_code:
                if self.expected_response_code == actual_response_code:
                    return True
                else:
                    return False
            else:
                # neither response action, nor response code are set
                return None

        return True




