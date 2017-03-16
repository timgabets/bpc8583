#!/usr/bin/env python

import socket
import sys
import struct
import os
import getopt

from ISO8583 import ISO8583, MemDump
from py8583spec import IsoSpec, IsoSpec1987BCD
 
def main(s):
    IsoMessage = ISO8583(IsoSpec=IsoSpec1987BCD())            
    IsoMessage.MTI("0210")
        
    IsoMessage.Field(2, 0)
    IsoMessage.Field(4, 1)
    IsoMessage.FieldData(4, 10000)
    IsoMessage.Field(13, 1)
    IsoMessage.FieldData(13, 1216)
    IsoMessage.Field(35, 0)
    IsoMessage.Field(52, 0)
    IsoMessage.Field(60, 0)

    IsoMessage.Print()

    data = IsoMessage.BuildIso()
    data = struct.pack("!H", len(data)) + data
             
    MemDump("Sending:", data)
    s.send(data)

    s.close()


def show_help(name):
    """
    Show help and basic usage
    """
    print('Usage: python3 {} [OPTIONS]... '.format(name))
    print('ISO8583 message client')
    print('  -p, --port=[PORT]\t\tTCP port to connect to, 1337 by default')
    print('  -s, --server=[IP]\t\tIP of the ISO host to connect to, 127.0.0.1 by default')


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 1337

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

    try:
        s = None
        for res in socket.getaddrinfo(ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            s = socket.socket(af, socktype, proto)
            s.connect(sa)
            main(s)
    except OSError as msg:
        print('Error connecting to {}:{} - {}'.format(ip, port, msg))
        sys.exit()
