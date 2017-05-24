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
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))   
            self.sock.listen(5)

        except OSError as msg:
            print('Error starting server - {}'.format(msg))
            sys.exit()
        print('Listening port *:{}'.format(self.port))


    def run(self):
        """
        """
        self.connect()

        while True:
            try:
                conn, addr = self.sock.accept()
                print ('Connected client: ' + addr[0] + ':' + str(addr[1]))

                while True:
                    data = conn.recv(4096)
                    if len(data) > 0:
                        trace('<< {} bytes received: '.format(len(data)), data)
                    
                    IsoMessage = ISO8583(data[2:], IsoSpec1987BPC())
                    IsoMessage.Print()
        
                    IsoMessage.MTI(get_response(IsoMessage.get_MTI()))            
                    IsoMessage.FieldData(39, '000')
                    # TODO: fix these fields:
                    IsoMessage.RemoveField(9)
                    IsoMessage.RemoveField(10)
                    IsoMessage.RemoveField(32)
                    IsoMessage.RemoveField(42)

                    IsoMessage.Print()
                    
                    data = IsoMessage.BuildIso()
                    #data = struct.pack("!H", len(data)) + data
                    data = get_message_length(data) + data
                    conn.send(data)
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
    print('  -p, --port=[PORT]\t\tTCP port to listen to, 3388 by default')


if __name__ == '__main__':
    ip = ''
    port = 3388
    max_conn = 5

    optlist, args = getopt.getopt(sys.argv[1:], 'hp:', ['help', 'port='])
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

    cbs = CBS(port=port)
    cbs.run()
