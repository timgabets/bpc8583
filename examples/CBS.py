#!/usr/bin/env python

import socket
import sys
import struct
import os
import getopt

from binascii import hexlify

from bpc8583.ISO8583 import ISO8583, MemDump, ParseError
from bpc8583.spec import IsoSpec, IsoSpec1987ASCII, IsoSpec1987BPC
from bpc8583.tools import get_response
from tracetools.tracetools import trace
from pynblock.tools import B2raw


def get_message_length(message):
    return B2raw(bytes(str(len(message)).zfill(4), 'utf-8'))


def get_balance_string(balance, currency_code):
    """
    Get balance string, according to Field 54 description
    """
    if not balance or not currency_code:
        return ''

    account_type = '00' # Not applicable or not specified
    amount_type = '01' # Deposit accounts: current (ledger) balance
    if float(balance) > 0:
        amount_sign = 'C'
    else:
        amount_sign = 'D'

    balance_formatted = balance.replace(' ', '').replace('.', '').replace('-', '').zfill(12)
    balance_string = account_type + amount_type + currency_code + amount_sign + balance_formatted

    return str(len(balance_string)) + balance_string


class CBS:
    def __init__(self, host=None, port=None):
        if host:
            self.host = host
        else:
            self.host = '127.0.0.1'

        if port:
            try:
                self.port = int(port)
            except ValueError:
                print('Invalid TCP port: {}'.format(arg))
                sys.exit()
        else:
            self.port = 3388


    def connect(self):
        """
        """
        try:
            self.sock = None
            for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                self.sock = socket.socket(af, socktype, proto)
                self.sock.connect(sa)
        except OSError as msg:
            print('Error connecting to {}:{} - {}'.format(self.host, self.port, msg))
            sys.exit()
        print('Connected to {}:{}'.format(self.host, self.port))


    def run(self):
        """
        """
        while True:
            try:
                self.connect()

                while True:
                    data = self.sock.recv(4096)
                    if len(data) > 0:
                        trace('<< {} bytes received: '.format(len(data)), data)
                    
                    request = ISO8583(data[2:], IsoSpec1987BPC())
                    request.Print()

                    response = ISO8583(data[2:], IsoSpec1987BPC())
                    response.MTI(get_response(request.get_MTI()))            
                    
                    processing_code = str(request.FieldData(3)).zfill(6)
                    
                    if processing_code[0:2] == '31':
                        response.FieldData(54, get_balance_string('1234.56', '826'))

                    response.FieldData(39, '000')
                    # TODO: fix these fields:
                    response.RemoveField(9)
                    response.RemoveField(10)
                    response.RemoveField(32)
                    response.RemoveField(42)

                    response.Print()
                    
                    data = response.BuildIso()
                    data = get_message_length(data) + data
                    self.sock.send(data)
                    trace('>> {} bytes sent:'.format(len(data)), data)
        
            except ParseError:
                print('Connection closed')
                conn.close()

        self.sock.close()
        conn.close()


def show_help(name):
    """
    Show help and basic usage
    """
    print('Usage: python3 {} [OPTIONS]... '.format(name))
    print('ISO8583 Core banking system simulator')
    print('  -p, --port=[PORT]\t\tTCP port to connect to, 3388 by default')
    print('  -s, --server=[IP]\t\tIP of the host to connect to, 127.0.0.1 by default')


if __name__ == '__main__':
    ip = ''
    port = 3388

    optlist, args = getopt.getopt(sys.argv[1:], 'hp:s:', ['help', 'port=', 'server='])
    for opt, arg in optlist:
        if opt in ('-h', '--help'):
            show_help(sys.argv[0])
            sys.exit()
        elif opt in ('-p', '--port'):
            try:
                port = int(arg)
            except ValueError:
                print('Invalid TCP port: {}'.format(arg))
                sys.exit()

        elif opt in ('-s', '--server'):
            ip = arg

    cbs = CBS(host=ip, port=port)
    cbs.run()
