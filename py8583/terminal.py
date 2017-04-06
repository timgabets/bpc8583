import socket
import sys

class Terminal:

    def __init__(self, host=None, port=None, id=None, merchant=None):
        """
        Terminal initialization
        """

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

        try:
            self.sock = None
            for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                self.sock = socket.socket(af, socktype, proto)
                self.sock.connect(sa)
        except OSError as msg:
            print('Error connecting to {}:{} - {}'.format(self.host, self.port, msg))
            sys.exit()


    def send(self, data):
        """
        """
        return self.sock.send(data)


    def recv(self):
        """
        """
        return self.sock.recv(4096)

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
