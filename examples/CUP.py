#!/usr/bin/env python

import getopt 
import sys
import socket
import struct
from time import sleep

from bpc8583.ISO8583 import ISO8583, MemDump, ParseError
from bpc8583.spec import IsoSpec, IsoSpec1987CUP
from bpc8583.tools import get_response, get_stan, get_time, trace_passed, trace_failed
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
        self.data = struct.pack("!H", int(str(len(self.data)), 16)) + self.data
        self.sock.send(self.data)

        trace(title='>> {} bytes sent:'.format(len(self.data)), data=self.data)


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


    def recv_logon_handshake(self):
        """
        """
        while True:            
            data = self.recv()
            request = ISO8583(data, IsoSpec1987CUP())
            request.Print()
    
            if request.get_MTI() != '0820' or request.FieldData(70) != 1:
                print('\tLogon failed')
                sleep(5)
            else:
                trace_passed("Sending SIGNON response", show_colored_description=True)

                response = self.init_response_message(request)
                MTI = str(request.get_MTI()).zfill(4)[-3:]
                response.Print()
                self.send(response.BuildIso())
                break

    def send_key_reset_request(self):
        trace_passed("Sending Key Reset request", show_colored_description=True)
        request = ISO8583(None, IsoSpec1987CUP())

        request.MTI('0800')
        request.FieldData(11, get_stan())
        request.FieldData(12, get_time())
        # Table 41. Field 53- Key Management Message Data Structure Definition
        # Key Type (n1): 1 - PIK, 2 - MAK
        # Encryption Method (n2): 0 - single length DES, 6 - double length DES
        # Reserved (n14): all set to 0
        request.FieldData(53, '1600000000000000')
        request.FieldData(70, 101)  # Union Pay resets the key
        
        request.Print()
        self.send(request.BuildIso())


    def init_response_message(self, request):
        """
        """
        response = ISO8583(None, IsoSpec1987CUP())
        response.MTI(get_response(request.get_MTI()))

        # Copy some key fields from original message:
        for field in [2, 3, 4, 5, 6, 7, 11, 12, 14, 15, 17, 24, 32, 33, 37, 48, 49, 50, 51, 70, 102]:
            response.FieldData(field, request.FieldData(field))
        return response


    def run(self):
        """
        """
        while True:
            try:
                self.connect()
                self.recv_logon_handshake()
                self.send_key_reset_request()

                while True:
                    data = self.recv() 
                    if not data:
                        raise ParseError

                    request = ISO8583(data, IsoSpec1987CUP())
                    request.Print()

                    response = self.init_response_message(request)

                    MTI = str(request.get_MTI()).zfill(4)[-3:]
                    response.Print()
                    self.send(response.BuildIso())
                
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