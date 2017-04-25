#!/usr/bin/env python

import sys
import os
import getopt
import time
import xml.etree.ElementTree as ET
from collections import OrderedDict

from bpc8583.ISO8583 import ISO8583, MemDump
from bpc8583.py8583spec import IsoSpec, IsoSpec1987BPC
from bpc8583.terminal import Terminal
from bpc8583.card import Card
from bpc8583.transaction import Transaction
from bpc8583.tools import trace_passed, trace_failed


class isoClient:
    def __init__(self, term, card, transactions=None):
        self.term = term
        self.card = card
        self.transactions = transactions


    def set_verbosity_level(self, verbosity_level):
        """
        """
        self.verbosity = verbosity_level


    def run(self):
        """
        """
        if self.transactions:
            self._run_non_interactive()
        else:
            self._run_interactive() 


    def _run_non_interactive(self):
        """
        """
        self.term.connect()
        for trxn in self.transactions:
            self.term.send(trxn.get_data(), show_trace=False)
            if self.verbosity:
                trxn.trace(header='Request')

            data = self.term.recv(show_trace=False)
            IsoMessage = ISO8583(data[2:], IsoSpec1987BPC())

            # Checking response code
            if trxn.is_response_expected(IsoMessage.FieldData(39)):
                trace_passed(trxn.get_description(), show_colored_description=self.verbosity)
                if self.verbosity:
                    IsoMessage.Print(header='Response')
            else:
                trace_failed(trxn.get_description(), IsoMessage.FieldData(39), show_colored_description=self.verbosity)
                trxn.trace(header='Request')
                IsoMessage.Print(header='Response')
    
        self.term.close()


    def _user_input(self, hint):
        """
        python-version-independent wrapper to raw_input()/input()
        """
        if sys.version[0] != '3':
            return raw_input(hint)
        else:
            return input(hint)


    def _show_available_transactions(self):
        """
        """
        print('e: echo')
        print('b: balance inquiry')
        print('p: manual purchase')


    def _run_interactive(self):
        """
        Run transactions interactively (by asking user which transaction to run)
        """
        self.term.connect()
        self._show_available_transactions()

        while True:
            trxn_type = self._user_input('\nEnter transaction to send: ')
        
            trxn = ''
            data = ''
            if trxn_type == 'e':
                trxn = Transaction('echo', self.card, self.term)
                trxn.trace()
        
            elif trxn_type == 'b':
                trxn = Transaction('balance', self.card, self.term)
                trxn.set_PIN(self._user_input('Enter PIN: '))
                trxn.trace()
        
            elif trxn_type == 'p':
                default_amount = 20000
                amount = self._user_input('Enter transaction amount ({} by default): '.format(default_amount))
                if not amount:
                    amount = default_amount

                trxn = Transaction('purchase', self.card, self.term)
                trxn.set_PIN(self._user_input('Enter PIN: '))
                trxn.set_amount(amount)
                trxn.trace()

            elif trxn_type == 'q':
                break

            else:
                print('Unknown transaction. Available transactions are:')
                self._show_available_transactions()
                continue
                
            self.term.send(trxn.get_data(), show_trace=verbosity)
            data = self.term.recv(show_trace=verbosity)
        
            IsoMessage = ISO8583(data[2:], IsoSpec1987BPC())
            IsoMessage.Print()
        
        self.term.close()


def parse_transaction_item(trxn, term, cards):
    """
    """
    t = None
    card = None

    try:
        card = cards[trxn.attrib['card']]
    except:
        for key, value in cards.items():
            card = value
            break        

    try:
        t = Transaction(trxn.attrib['type'], card, term)
    except KeyError:
        print('Error parsing {}: transaction type is not set'.format(filename))
        sys.exit()

    try:
        t.set_description(trxn.attrib['description'])
    except KeyError:
        pass

    for attrib in trxn:
        if attrib.tag.lower() == 'amount':
            t.set_amount(attrib.text)
        if attrib.tag.lower() == 'pin':
            t.set_PIN(attrib.text)
        elif attrib.tag.lower() == 'response_code':
            t.set_expected_code(attrib.text)
        elif attrib.tag.lower() == 'response_action':
            if not t.set_expected_action(attrib.text):
                print('Unknown response action: {}'.format(attrib.text))

    return t


def parse_card_data(card):
    """
    """
    pan = None
    expiry_date = None
    service_code = None
    PVVKi = None
    PVV = None
    CVV = None
    discr_data = None

    for attrib in card:
        if attrib.tag.lower() == 'pan':
            pan = attrib.text
        if attrib.tag.lower() == 'expiry_date':
            expiry_date = attrib.text
        elif attrib.tag.lower() == 'service_code':
            service_code = attrib.text
        elif attrib.tag.lower() == 'pvvki':
            PVVKi = attrib.text
        elif attrib.tag.lower() == 'pvv':
            PVV = attrib.text
        elif attrib.tag.lower() == 'cvv':
            CVV = attrib.text
        elif attrib.tag.lower() == 'discr_data':
            discr_data = attrib.text

    return Card(pan=pan, expiry_date=expiry_date, service_code=service_code, pvvki=PVVKi, PVV=PVV, CVV=CVV, discretionary_data=discr_data)
            

def parse_data_file(filename, term):
    """
    """
    data_tree = ET.parse(filename)
    data_root = data_tree.getroot()

    cards = OrderedDict()
    for item in data_root:
        if item.tag == 'card':
            c = parse_card_data(item)
            if c:
                cards[c.get_str_card_number()] = c

    if not cards:
        # No <card> items in transaction file:
        c = Card()
        cards[c.get_str_card_number()] = c

    transactions = []
    for item in data_root:
        if item.tag == 'trxn':
            t = parse_transaction_item(item, term, cards)
            if t:
                transactions.append(t)

    return transactions


def show_help(name):
    """
    Show help and basic usage
    """
    print('Usage: python3 {} [OPTIONS]... '.format(name))
    print('ISO8583 message client')
    print('  -v, --verbose\t\tRun transactions verbosely')
    print('  -p, --port=[PORT]\t\tTCP port to connect to, 1337 by default')
    print('  -s, --server=[IP]\t\tIP of the ISO host to connect to, 127.0.0.1 by default')
    print('  -t, --terminal=[ID]\t\tTerminal ID (used in DE 41 ISO field, 10001337 by default)')
    print('  -m, --merchant=[ID]\t\tMerchant ID (used in DE 42 ISO field, 999999999999001 by default)')
    print('  -f, --file=[file.xml]\t\tUse transaction data from the given XML-file')


if __name__ == '__main__':
    verbosity = False
    ip = None
    port = None
    terminal_id = None
    merchant_id = None
    data_file = None
    transactions = None

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hp:s:t:m:f:v', ['help', 'port=', 'server=', 'terminal=', 'merchant=', 'file=', 'verbose'])
        for opt, arg in optlist:
            if opt in ('-v', '--verbose'):
                verbosity = True

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
                data_file = arg

    except getopt.GetoptError:
        show_help(sys.argv[0])
        sys.exit()
    
    term = Terminal(host=ip, port=port, id=terminal_id, merchant=merchant_id)
    if data_file:
        transactions = parse_data_file(data_file, term)

    pos = isoClient(term, Card(), transactions)
    pos.set_verbosity_level(verbosity)
    pos.run()
