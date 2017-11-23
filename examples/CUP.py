#!/usr/bin/env python

import getopt 
import sys
import socket
import struct

from bpc8583.ISO8583 import ISO8583, MemDump, ParseError
from bpc8583.spec import IsoSpec, IsoSpec1987BPC
from bpc8583.tools import get_response, get_stan, get_datetime_with_year
from tracetools.tracetools import trace


class CUP:
    def __init__(self, host=None, port=None):
        self.host = host if host else '127.0.0.1'
        self.header = 'DEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFFF0000'

        if port:
            try:
                self.port = int(port)
            except ValueError:
                print('Invalid TCP port: {}'.format(arg))
                sys.exit()
        else:
            self.port = 8989

        self.responses = {'Approval': '000', 'Invalid Amount': '903', 'Invalid account number': '914', 'Insufficient funds': '915', }


    def recv(self):
        """
        """
        data = self.sock.recv(4096)
        if len(data) > 0:
            trace(title='<< {} bytes received: '.format(len(data)), data=data)
            return data[48:]
        else:
            return None


    def send(self, data):
        """
        """
        self.data = self.header.encode('latin') + data
        self.sock.send(struct.pack("!H", int(str(len(self.data)), 16)) + self.data)
        trace(title='>> {} bytes sent:'.format(len(data)), data=self.data)


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


    def send_logon_handshake(self):
        """
        """
        while True:
            request = ISO8583(None, IsoSpec1987BPC())
    
            request.MTI('0820')
            request.FieldData(11, get_stan())
            request.FieldData(12, get_datetime_with_year())
            request.FieldData(70, 1)
    
            request.Print()
            data = request.BuildIso()
            self.send(data)
    
            data = self.recv()
            response = ISO8583(data, IsoSpec1987BPC())
            response.Print()
    
            if response.get_MTI() != '0814' or response.FieldData(24) != 801 or response.FieldData(39) != '000':
                print('\tLogon failed')
                sleep(5)
            else:
                break


    def run(self):
        """
        """
        while True:
            try:
                self.connect()
                self.send_logon_handshake()

                while True:
                    data = self.recv() 
                    if not data:
                        raise ParseError

                    """
                    request = ISO8583(data, IsoSpec1987BPC())
                    request.Print()

                    response = self.init_response_message(request)

                    MTI = str(request.get_MTI()).zfill(4)[-3:]
                    trxn_type = self.get_transaction_type(request)
                    card_number = request.FieldData(2)
                    currency_code = request.FieldData(51)

                    if MTI in ['100', '200']:
                        # Authorization request or financial request
                        if not self.db.card_exists(card_number):
                            # TODO: command line option to add cards autmatically
                            print('\nWARNING: Card {} does not exist!\n'.format(card_number));
                            self.db.insert_card_record(card_number, currency_code, 0);

                        if trxn_type == '31':
                            # Balance
                            self.process_trxn_balance_inquiry(request, response)
                        elif trxn_type in ['00', '01', '50']:
                            # Purchase or ATM Cash
                            self.process_trxn_debit_account(request, response)
                        elif trxn_type == '39':
                            # Ministatement
                            self.process_statement_request(request, response)
                        elif trxn_type == '88':
                            # Cardholder name inquiry
                            self.process_cardholder_name_inquiry(request, response)
                        else:
                            print('Unsupported transaction type {}. Responding APPROVAL by default'.format(trxn_type))
                            response.FieldData(39, self.responses['Approval'])

                    elif MTI in ['120']:
                        # Authorization advice
                        if trxn_type in ['00', '01']:
                            # Purchase or ATM Cash
                            self.settle_auth_advice(request, response)
                        else:
                            response.FieldData(39, self.responses['Approval'])

                    elif MTI in ['400', '420']:
                        # Reversal
                        if trxn_type in ['00', '01']:
                            # Purchase or ATM Cash
                            self.settle_reversal(request, response)

                    response.Print()
                    
                    data = response.BuildIso()
                    data = self.get_message_length(data) + data
                    self.send(data)
                    """
        
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
    print('China Union Pay dummy network simulator')
    print('  -p, --port=[PORT]\t\tTCP port to connect to, 8989 by default')


if __name__ == '__main__':
    ip = ''
    port = 8989

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

    cbs = CUP(host=ip, port=port)
    cbs.run()