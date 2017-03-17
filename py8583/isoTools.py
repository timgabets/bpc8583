from ISO8583 import Dump
from time import gmtime, strftime
 
def get_timestamp(t=None):
    """
    """
    return strftime('%H:%M:%S', gmtime())

def trace(title, data):
    """
    """
    print('\n{} {}\n{}'.format(get_timestamp(), title, Dump(data)))
