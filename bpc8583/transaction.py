import struct

from ISO8583 import ISO8583
from isoTools import trace, get_datetime_with_year, get_datetime, get_stan
from py8583spec import IsoSpec, IsoSpec1987BPC
from datetime import datetime

class Transaction():
    def __init__(self, _type, _card, _term):
        """
        """
        self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
        self.card = _card
        self.term = _term
        self.type = _type.lower()
        self.description = ''
        self.expected_response_code = None

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
            
            self.IsoMessage.FieldData(2, card.get_card_number())
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
            return
    
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
        """
        if self.description:
            return self.description
        else:
            return self.type + ' ' + str(self.IsoMessage.FieldData(11))



    def set_PIN(self, PIN):
        """
        """
        if PIN:
            self.IsoMessage.FieldData(52, self.term.get_encrypted_pin(PIN, self.card.get_card_number()))
            self.rebuild()


    def set_amount(self, amount):
        """
        Set transaction amount
        """
        if amount:
            self.IsoMessage.FieldData(4, int(amount))
            self.rebuild()


    def set_expected(self, expected_response):
        """
        Expected outcome of the transaction
        """
        self.expected_response_code = expected_response


    def get_expected(self):
        """
        """
        return self.expected_response_code


