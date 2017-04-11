#!/usr/bin/env python

import sys
import struct
import os
import getopt
import time
import random

from ISO8583 import ISO8583, MemDump
from isoTools import trace, get_datetime
from py8583spec import IsoSpec, IsoSpec1987BPC
from terminal import Terminal
from card import Card

def balance_enquiry(card, terminal_id, merchant_id, currency_code):
    """
    Balance Enguiry
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
    IsoMessage.FieldData(22, 20)
    IsoMessage.FieldData(24, 100)
    IsoMessage.FieldData(25, 0)
    IsoMessage.FieldData(35, card.get_track2())
    IsoMessage.FieldData(41, terminal_id)
    IsoMessage.FieldData(42, merchant_id)
    #IsoMessage.FieldData(49, currency_code)

    IsoMessage.Print()
    return IsoMessage.BuildIso()


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


def main(term, card):
    """
    # ECHO
    data = echo_test(term.get_terminal_id(), term.get_merchant_id())
    data = struct.pack("!H", len(data)) + data
             
    term.send(data)
    data = term.recv()

    IsoMessage = ISO8583(data[2:], IsoSpec1987BPC())
    IsoMessage.Print()
    """

    # BENQ
    data = balance_enquiry(card, term.get_terminal_id(), term.get_merchant_id(), term.get_currency_code())
    data = struct.pack("!H", len(data)) + data
             
    term.send(data)
    data = term.recv()

    IsoMessage = ISO8583(data[2:], IsoSpec1987BPC())
    IsoMessage.Print()

    term.close()


def show_help(name):
    """
    Show help and basic usage
    """
    print('Usage: python3 {} [OPTIONS]... '.format(name))
    print('ISO8583 message client')
    print('  -p, --port=[PORT]\t\tTCP port to connect to, 1337 by default')
    print('  -s, --server=[IP]\t\tIP of the ISO host to connect to, 127.0.0.1 by default')
    print('  -t, --terminal=[ID]\t\tTerminal ID (used in DE 41 ISO field, 10001337 by default)')
    print('  -m, --merchant=[ID]\t\tMerchant ID (used in DE 42 ISO field, 999999999999001 by default)')


if __name__ == '__main__':
    ip = None
    port = None
    terminal_id = None
    merchant_id = None

    optlist, args = getopt.getopt(sys.argv[1:], 'hp:s:t:m:', ['help', 'port=', 'server=', 'terminal=', 'merchant='])
    for opt, arg in optlist:
        if opt in ('-h', '--help'):
            show_help(sys.argv[0])
            sys.exit()

        elif opt in ('-p', '--port'):
            port = arg

        elif opt in ('-s', '--server'):
            ip = arg

        elif opt in ('-t', '--terminal'):
            terminal_id = arg

        elif opt in ('-m', '--merchant'):
            merchant_id = arg
    
    term = Terminal(host=ip, port=port, id=terminal_id, merchant=merchant_id)
    card = Card()
    main(term, card)
