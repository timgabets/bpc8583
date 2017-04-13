import struct

from ISO8583 import ISO8583
from isoTools import trace, get_datetime_with_year, get_datetime, get_stan
from py8583spec import IsoSpec, IsoSpec1987BPC
from datetime import datetime

class Transaction():
    def __init__(self, type, card, term, PIN=None, amount=None):
        """
        """
        self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())

        if type == 'echo':
            """
            """
            self.IsoMessage.MTI("0800")

            self.IsoMessage.FieldData(3, 990000)
            self.IsoMessage.FieldData(12, get_datetime_with_year())


        elif type == 'balance':
            """
            """
            self.IsoMessage.MTI("0100")
            
            self.IsoMessage.FieldData(2, card.get_card_number())
            self.IsoMessage.FieldData(3, 310000)
            self.IsoMessage.FieldData(4, 0)
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(13, 1216)
            self.IsoMessage.FieldData(22, term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, card.get_track2())

        elif type == 'purchase':
            """
            """
            self.IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())            
            self.IsoMessage.MTI("0200")
        
            self.IsoMessage.FieldData(2, card.get_card_number())
            self.IsoMessage.FieldData(3, 000000)
            self.IsoMessage.FieldData(4, int(amount))
            self.IsoMessage.FieldData(12, get_datetime_with_year())
            self.IsoMessage.FieldData(22, term.get_pos_entry_mode())
            self.IsoMessage.FieldData(24, 100)
            self.IsoMessage.FieldData(25, 0)
            self.IsoMessage.FieldData(35, card.get_track2())

        else:
            return
    
        # Common message fields:
        self.IsoMessage.FieldData(7, get_datetime())
        self.IsoMessage.FieldData(11, get_stan())
        self.IsoMessage.FieldData(41, term.get_terminal_id())
        self.IsoMessage.FieldData(42, term.get_merchant_id())
        self.IsoMessage.FieldData(49, term.get_currency_code())
        if PIN:
            self.IsoMessage.FieldData(52, term.get_encrypted_pin(PIN, card.get_card_number()))

        self.IsoMessage.Print()
        self.data = self.IsoMessage.BuildIso()

    def get_data(self):
        return struct.pack("!H", len(self.data)) + self.data

    def set_pin(self, PIN):
        pass
