import socket
import struct
import sys

from bpc8583.tools import get_datetime, get_random_hex
from tracetools.tracetools import trace
from pynblock.tools import raw2str, get_pinblock
from Crypto.Cipher import DES3


class Terminal:

    def __init__(self, host=None, port=None, id=None, merchant=None, master_key=None, terminal_key=None, show_keys=None):
        """
        Terminal initialization
        """
        self.pinblock_format = '01'

        # Host to connect to
        self.host = host if host else '127.0.0.1'
    
        # Port ot connect to
        try:
            self.port = int(port) if port else 1337
        except ValueError:
            raise ValueError('Invalid TCP port: {}'.format(port))

        # Terminal ID
        self.terminal_id = id if id else '10001337'

        # Merchant ID
        self.merchant_id = merchant if merchant else '999999999999001'

        self.currency = '643'
        self.country_code = '643'
        
        # Keys
        self.keyfile_name = '.terminalkey.cache'
        self.master_key = bytes.fromhex(master_key) if master_key else bytes.fromhex('CF7730DBA6CAC5E13C3FB45CAF8D71E1')    

        if terminal_key:
            self.terminal_key = bytes.fromhex(terminal_key)
        else:
            stored_key = self.get_stored_key()
            if stored_key:
                self.terminal_key = bytes.fromhex(stored_key)
            else:
                self.terminal_key = bytes.fromhex('FA9F90D49CB27B7D14A3FA9CCCFF6CB7')
                self.store_terminal_key(raw2str(self.terminal_key))

        self.tpk_cipher = DES3.new(self.terminal_key, DES3.MODE_ECB)
        self.tmk_cipher = DES3.new(self.master_key, DES3.MODE_ECB)

        self.show_keys = show_keys
        self.print_keys()


    def print_keys(self):
        if self.show_keys:
            print('  Master key: {}'.format(raw2str(self.master_key)))
            print('Terminal key: {}'.format(raw2str(self.terminal_key)))
        

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


    def store_terminal_key(self, key):
        """
        """
        try:
            f = open(self.keyfile_name, 'w+')
            f.write(key)
            f.close()
        except:
            return False
        return True


    def get_stored_key(self):
        """
        """
        try:
            f = open(self.keyfile_name, 'r')
            key = f.read()
            f.close()
            return key
        except:
            return None


    def set_terminal_key(self, encrypted_key):
        """
        Change the terminal key. The encrypted_key is a hex string.
        encrypted_key is expected to be encrypted under master key
        """
        if encrypted_key:
            try:
                new_key = bytes.fromhex(encrypted_key)
                if len(self.terminal_key) != len(new_key):
                    # The keys must have equal length
                    return False

                self.terminal_key = self.tmk_cipher.decrypt(new_key)
                self.store_terminal_key(raw2str(self.terminal_key))

                self.tpk_cipher = DES3.new(self.terminal_key, DES3.MODE_ECB)
                self.print_keys()
                return True

            except ValueError:
                return False

        return False


    def get_terminal_key(self):
        """
        Get string representation of terminal key (needed mostly for debugging purposes)
        """
        return raw2str(self.terminal_key)


    def get_encrypted_pin(self, clear_pin, card_number):
        """
        Get PIN block in ISO 0 format, encrypted with the terminal key
        """
        if not self.terminal_key:
            print('Terminal key is not set')
            return ''

        if self.pinblock_format == '01':
            try:
                pinblock = bytes.fromhex(get_pinblock(clear_pin, card_number))
                #print('PIN block: {}'.format(raw2str(pinblock)))
            except TypeError:
                return ''

            encrypted_pinblock = self.tpk_cipher.encrypt(pinblock)
            return raw2str(encrypted_pinblock)

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
