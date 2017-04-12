import socket
import sys
from isoTools import trace, get_datetime

class Terminal:

    def __init__(self, host=None, port=None, id=None, merchant=None):
        """
        Terminal initialization
        """
        self.pinblock_format = '01'
        self.key = b'0000000000000000'

        # Host to connect to
        if host:
            self.host = host
        else:
            self.host = '127.0.0.1'

        # Port ot connect to
        if port:
            try:
                self.port = int(port)
            except ValueError:
                print('Invalid TCP port: {}'.format(arg))
                sys.exit()
        else:
            self.port = 1337

        # Terminal ID
        if id:
            self.terminal_id = id
        else:
            self.terminal_id = '10001337'

        # Merchant ID
        if merchant:
            self.merchant_id = merchant
        else:
            self.merchant_id = '999999999999001'

        self.currency = '643'


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


    def send(self, data):
        """
        """
        trace('>> {} bytes sent:'.format(len(data)), data)
        return self.sock.send(data)


    def recv(self):
        """
        """
        data = self.sock.recv(4096)
        trace('<< {} bytes received: '.format(len(data)), data)
        return data

    def close(self):
        """
        """
        self.sock.close()


    def get_terminal_id(self):
        """
        """
        return self.terminal_id


    def get_merchant_id(self):
        """
        """
        return self.merchant_id


    def get_currency_code(self):
        """
        """
        return self.currency


    def get_pinblock(self, PIN, PAN):
        """
        """
        if not PIN or not PAN:
            return None

        block1 = '0' + str(len(PIN)) + str(PIN)
        while len(block1) < 16:
            block1 += 'F'
        return block1


    def get_encrypted_pin(self, clear_pin):
        """
        TODO
        """
        if self.pinblock_format == '01':

            return 'ABCDEF09'
        else:
            print('Unsupported PIN Block format')
            return ''

    def get_pos_entry_mode(self):
        """
        """
        pan_and_date_entry_mode = '90'
        pin_entry_capability = '1'
        return int(pan_and_date_entry_mode + pin_entry_capability)


