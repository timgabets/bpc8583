import random

from ISO8583 import ISO8583
from isoTools import trace, get_datetime
from py8583spec import IsoSpec, IsoSpec1987BPC

def echo_test(terminal_id, merchant_id):
    """
    Echo
    """
    IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())
    IsoMessage.MTI("0800")

    IsoMessage.FieldData(3, 990000)
    IsoMessage.FieldData(7, get_datetime())
    IsoMessage.FieldData(11, random.randint(0, 999999))
    IsoMessage.FieldData(41, terminal_id)
    IsoMessage.FieldData(42, merchant_id)

    IsoMessage.Print()
    return IsoMessage.BuildIso()


def balance_inquiry(card, terminal_id, merchant_id, currency_code):
    """
    Balance Inguiry
    """
    IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())            
    IsoMessage.MTI("0100")
        
    IsoMessage.FieldData(2, card.get_card_number())
    IsoMessage.FieldData(3, 310000)
    IsoMessage.FieldData(4, 0)
    IsoMessage.FieldData(7, get_datetime())
    IsoMessage.FieldData(11, random.randint(0, 999999))
    IsoMessage.FieldData(12, 104956)
    IsoMessage.FieldData(13, 1216)
    IsoMessage.FieldData(22, 20)
    IsoMessage.FieldData(24, 100)
    IsoMessage.FieldData(25, 0)
    IsoMessage.FieldData(35, card.get_track2())
    IsoMessage.FieldData(41, terminal_id)
    IsoMessage.FieldData(42, merchant_id)
    #IsoMessage.FieldData(49, currency_code)

    IsoMessage.Print()
    return IsoMessage.BuildIso()