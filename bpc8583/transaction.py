import struct

from ISO8583 import ISO8583
from isoTools import trace, get_datetime_with_year, get_datetime, get_stan
from py8583spec import IsoSpec, IsoSpec1987BPC
from datetime import datetime

class Transaction():
    def __init__(self, type, card, term, amount=None):
        """
        """
        IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())

        if type == 'echo':
            """
            """
            IsoMessage.MTI("0800")

            IsoMessage.FieldData(3, 990000)

        elif type == 'balance':
            """
            """
            IsoMessage.MTI("0100")
            
            IsoMessage.FieldData(2, card.get_card_number())
            IsoMessage.FieldData(3, 310000)
            IsoMessage.FieldData(4, 0)
            IsoMessage.FieldData(12, get_datetime_with_year())
            IsoMessage.FieldData(13, 1216)
            IsoMessage.FieldData(22, 20)
            IsoMessage.FieldData(24, 100)
            IsoMessage.FieldData(25, 0)
            IsoMessage.FieldData(35, card.get_track2())

        elif type == 'purchase':
            """
            """
            IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())            
            IsoMessage.MTI("0200")
        
            IsoMessage.FieldData(2, card.get_card_number())
            IsoMessage.FieldData(3, 000000)
            IsoMessage.FieldData(4, int(amount))
            IsoMessage.FieldData(12, get_datetime_with_year())
            IsoMessage.FieldData(22, 20)
            IsoMessage.FieldData(24, 100)
            IsoMessage.FieldData(25, 0)

        else:
            return
    
        # Common message fields:
        IsoMessage.FieldData(7, get_datetime())
        IsoMessage.FieldData(11, get_stan())
        IsoMessage.FieldData(41, term.get_terminal_id())
        IsoMessage.FieldData(42, term.get_merchant_id())
        IsoMessage.FieldData(49, term.get_currency_code())

        IsoMessage.Print()
        self.data = IsoMessage.BuildIso()

    def get_data(self):
        return struct.pack("!H", len(self.data)) + self.data
