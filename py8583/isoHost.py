#!/usr/bin/env python

import socket
import sys
import struct
import os
import getopt

from ISO8583 import ISO8583, MemDump
from py8583spec import IsoSpec
 
def main(s):
    while True:
        try:
            conn, addr = s.accept()
            print ('Connected client: ' + addr[0] + ':' + str(addr[1]))
            data = conn.recv(4096)
            MemDump("Data received:", data)
            
            Len = struct.unpack_from("!H", data[:2])[0]
            
            if(Len != len(data) - 2):
                print("Invalid length {0} - {1}".format(Len, len(data) - 2))
                conn.close()
                continue
            
            IsoMessage = ISO8583(data[2:], IsoSpec1987BCD())
            
            IsoMessage.PrintMessage()
            
            IsoMessage.MTI("0210")
            
            IsoMessage.Field(39, 1)
            IsoMessage.FieldData(39, "00")
            IsoMessage.Field(2, 0)
            IsoMessage.Field(35, 0)
            IsoMessage.Field(52, 0)
            IsoMessage.Field(60, 0)
             
            print("\n\n\n")
            IsoMessage.PrintMessage()
            data = IsoMessage.BuildIso()
            data = struct.pack("!H", len(data)) + data
             
            MemDump("Sending:", data)
            conn.send(data)
            
        except KeyboardInterrupt:
            print('Exit')
            s.close()
            sys.exit()
        except Exception as ex:
            print(ex)
            
        conn.close()


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
