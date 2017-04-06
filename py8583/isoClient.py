#!/usr/bin/env python

import socket
import sys
import struct
import os
import getopt
import time
import random

from ISO8583 import ISO8583, MemDump
from isoTools import trace, get_datetime
from py8583spec import IsoSpec, IsoSpec1987BCD, IsoSpec1987ASCII, IsoSpec1987BPC

def send_balance_enquiry():
    IsoMessage = ISO8583(IsoSpec=IsoSpec1987ASCII())            
    IsoMessage.MTI("0100")
        
    IsoMessage.SetBitmap([2, 3, 4, 7, 11, 12, 13, 22, 24, 25, 35, 41, 49])

    IsoMessage.FieldData(2, 5555011012400477)
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
    IsoMessage.FieldData(35, '4290011012400477=18091011872300000720')
    IsoMessage.FieldData(41, 'P0000001')
    IsoMessage.FieldData(42, '00000000M000007')
    IsoMessage.FieldData(49, '643')

    IsoMessage.Print()
    return IsoMessage.BuildIso()


def send_echo_test():
    IsoMessage = ISO8583(IsoSpec=IsoSpec1987BCD())        
    #IsoMessage = ISO8583(IsoSpec=IsoSpec1987BPC())       
    IsoMessage.MTI("0800")

    IsoMessage.SetBitmap([3, 7, 11, 24, 41, 42])

    IsoMessage.FieldData(3, 990000)
    IsoMessage.FieldData(7, get_datetime())
    IsoMessage.FieldData(11, random.randint(0, 999999))
    IsoMessage.FieldData(24, 831)
    IsoMessage.FieldData(41, '1000026')
    IsoMessage.FieldData(42, '00000000M000007')

    IsoMessage.Print()
    return IsoMessage.BuildIso()


def main(s):
    data = send_echo_test()
    data = struct.pack("!H", len(data)) + data
             
    trace('>> {} bytes sent:'.format(len(data)), data)
    s.send(data)

    data = s.recv(4096)
    trace('<< {} bytes received: '.format(len(data)), data)
    IsoMessage = ISO8583(data[2:], IsoSpec1987BCD())
    IsoMessage.Print()

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
