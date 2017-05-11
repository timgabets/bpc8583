#!/usr/bin/env python

import socket
import sys
import struct
import os
import getopt

from bpc8583.ISO8583 import ISO8583, MemDump
from bpc8583.spec import IsoSpec, IsoSpec1987BPC
from bpc8583.tools import get_response
from tracetools.tracetools import trace

def main(s):
    while True:
        conn, addr = s.accept()
        print ('Connected client: ' + addr[0] + ':' + str(addr[1]))

        while True:
            try:
                data = conn.recv(4096)
                trace('<< {} bytes received: '.format(len(data)), data)
                    
                Len = struct.unpack_from("!H", data[:2])[0]
                
                if(Len != len(data) - 2):
                    print("Invalid length {0} - {1}".format(Len, len(data) - 2))
                    conn.close()
                    continue
                
                IsoMessage = ISO8583(data[2:], IsoSpec1987BPC())
                IsoMessage.Print()
                
                IsoMessage.MTI(get_response(IsoMessage.get_MTI()))
                
                IsoMessage.Field(39, 1)
                IsoMessage.FieldData(39, '000')
                IsoMessage.Field(2, 0)
                IsoMessage.Field(35, 0)
                IsoMessage.Field(52, 0)
                IsoMessage.Field(60, 0)
                 
                IsoMessage.Print()
                data = IsoMessage.BuildIso()
                data = struct.pack("!H", len(data)) + data
                
                conn.send(data)
                trace('>> {} bytes sent:'.format(len(data)), data)

            except KeyboardInterrupt:
                print('Exit')
                s.close()
                sys.exit()

            #except:
            #    conn.close()
            #    print('Connection closed')
            #    break   

def show_help(name):
    """
    Show help and basic usage
    """
    print('Usage: python3 {} [OPTIONS]... '.format(name))
    print('ISO8583 message echo server')
    print('  -p, --port=[PORT]\t\tTCP port to listen, 1337 by default')


if __name__ == '__main__':
    ip = ''
    port = 1337
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

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))   
        s.listen(max_conn)
        print('Listening on port {}'.format(port))
        main(s)
    except OSError as msg:
        print('Error starting server: {}'.format(msg))
        sys.exit()
