#!/usr/bin/env python

import sys
import os
import getopt
import time
import xml.etree.ElementTree as ET

from ISO8583 import ISO8583, MemDump
from py8583spec import IsoSpec, IsoSpec1987BPC
from terminal import Terminal
from card import Card
from transaction import Transaction


def show_available_transactions():
    print('e: echo')
    print('b: balance inquiry')
    print('p: manual purchase')


def user_input(hint):
    """
    python-version-independent wrapper to raw_input()/input()
    """
    if sys.version[0] != '3':
        return raw_input(hint)
    else:
        return input(hint)


def interactive(term, card):
    """
    Run transactions interactively (by asking user which transaction to run)
    """
    term.connect()
    show_available_transactions()

    while True:
        trxn_type = user_input('\nEnter transaction to send: ')
    
        trxn = ''
        data = ''
        if trxn_type == 'e':
            trxn = Transaction('echo', card, term)
            trxn.trace()
    
        elif trxn_type == 'b':
            trxn = Transaction('balance', card, term)
            trxn.set_PIN(user_input('Enter PIN: '))
            trxn.trace()
    
        elif trxn_type == 'p':
            default_amount = 1000
            amount = user_input('Enter transaction amount ({} by default): '.format(default_amount))
            if not amount:
                amount = default_amount

            trxn = Transaction('purchase', card, term)
            trxn.set_PIN(user_input('Enter PIN: '))
            trxn.set_amount(amount)
            trxn.trace()

        elif trxn_type == 'q':
            break

        else:
            print('Unknown transaction. Availbale transactions are:')
            show_available_transactions()
            continue
            
        term.send(trxn.get_data())
        data = term.recv()
    
        IsoMessage = ISO8583(data[2:], IsoSpec1987BPC())
        IsoMessage.Print()
    
    term.close()


def main(term, card, transactions=None):
    """
    """
    if transactions:
        term.connect()
        for trxn in transactions:
            pass
        term.close()
    else:
       interactive(term, card) 


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
    print('  -f, --file=[file.xml]\t\tUse transaction data from the given XML-file')


def parse_transactions_file(filename, term, card):
    transactions = []
    trxn_tree = ET.parse(filename)
    trxn_root = trxn_tree.getroot()
    for trxn in trxn_root:
        print('=======')
        trxn_details = trxn.attrib
        print(trxn_details)
        for attrib in trxn:
            print(attrib.tag, attrib.text)
            #if attrib.tag == 'amount':
            #    amount = attrib.text
            #elif attrib.tag == 'currency':
            #    currency = attrib.text

            #t = Transaction('echo', card, term)

    sys.exit()
    return transactions


if __name__ == '__main__':
    ip = None
    port = None
    terminal_id = None
    merchant_id = None
    trxn_file = None
    transactions = None

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hp:s:t:m:f:', ['help', 'port=', 'server=', 'terminal=', 'merchant=', 'file='])
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

            elif opt in ('-f', '--file'):
                trxn_file = arg

    except getopt.GetoptError:
        show_help(sys.argv[0])
        sys.exit()
    
    term = Terminal(host=ip, port=port, id=terminal_id, merchant=merchant_id)
    card = Card()
    if trxn_file:
        transactions = parse_transactions_file(arg, term, card)
    main(term, card, transactions)
