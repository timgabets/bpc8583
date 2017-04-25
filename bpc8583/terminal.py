import socket
import struct
import sys
import binascii

from bpc8583.tools import trace, get_datetime, get_random_hex

from Crypto.Cipher import DES3


class Terminal:

    def __init__(self, host=None, port=None, id=None, merchant=None, key=None):
        """
        Terminal initialization
        """
        self.pinblock_format = '01'

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
        self.country_code = '643'

        # Terminal key
        if key:
            self.key = bytes.fromhex(key)
        else:
            self.key = bytes.fromhex('deadbeef deadbeef deadbeef deadbeef')

        # Crypto init
        self.cipher = DES3.new(self.key, DES3.MODE_ECB)


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


    def send(self, data, show_trace=True):
        """
        """
        if show_trace:
            trace('>> {} bytes sent:'.format(len(data)), data)
        return self.sock.send(data)


    def recv(self, show_trace=True):
        """
        """
        data = self.sock.recv(4096)
        if show_trace:
            trace('<< {} bytes received: '.format(len(data)), data)
        return data

    def close(self):
        """
        """
        print('Disconnected from {}'.format(self.host))
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


    def set_terminal_key(self, key_value):
        """
        Set the terminal key. The key_value is a hex string
        key_value is expected to be encrypted under existing key
        """
        if key_value:
            try:
                new_key = bytes.fromhex(key_value)
                if len(self.key) != len(new_key):
                    # The keys must have equal length
                    return False

                self.key = self.cipher.decrypt(new_key)
                self.cipher = DES3.new(self.key, DES3.MODE_ECB)
                return True

            except ValueError:
                return False

        return False


    def get_terminal_key(self):
        """
        Get string representation of terminal key (needed mostly for debugging purposes)
        """
        return binascii.hexlify(self.key).decode('utf-8').upper()


    def _get_pinblock(self, __PIN, __PAN):
        """
        """
        PIN = str(__PIN)
        PAN = str(__PAN)

        if not PIN or not PAN:
            return None

        block1 = '0' + str(len(PIN)) + str(PIN)
        while len(block1) < 16:
            block1 += 'F'
        block2 = '0000' + PAN[:12]

        try:
            raw_message = bytes.fromhex(block1)
            raw_key = bytes.fromhex(block2)
        except ValueError:
            return ''

        result = ''.join(["{0:#0{1}x}".format((i ^ j), 4)[2:] for i, j in zip(raw_message, raw_key)])

        return result


    def get_encrypted_pin(self, clear_pin, card_number):
        """
        Get PIN block in ISO 0 format, encrypted with the terminal key
        """
        if not self.key:
            print('Terminal key is not set')
            return ''

        if self.pinblock_format == '01':
            try:
                pinblock = bytes.fromhex(self._get_pinblock(clear_pin, card_number))
            except TypeError:
                return ''

            encrypted_pinblock = self.cipher.encrypt(pinblock)
            return binascii.hexlify(encrypted_pinblock).decode('utf-8').upper()

        else:
            print('Unsupported PIN Block format')
            return ''

    def get_pos_entry_mode(self):
        """
        """
        pan_and_date_entry_mode = '90'
        pin_entry_capability = '0'
        return int(pan_and_date_entry_mode + pin_entry_capability)


    def get_tvr(self):
        """
        return TVR (The status of the different functions as seen from the terminal)
        TODO: non-dummy value
        """
        return '0000040880'


    def get_unpredno(self):
        """
        Get unpredictable number (a value to provide variability and uniqueness to the generation of a cryptogram), used in ICC data
        """
        return get_random_hex(8)


    def get_country_code(self):
        """
        Get terminal country code, used in ICC data
        """
        return self.country_code.rjust(4, '0')
