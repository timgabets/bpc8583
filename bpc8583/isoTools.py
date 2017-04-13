import random

from time import strftime
from datetime import datetime

def dump(data):
    """
    Memdump with no title
    """
    i = 1

    if( isinstance(data, bytes) == False ):
        raise TypeError("Expected bytes for data")

    dump = '\t'
    dump_ascii = ''
    padding = '        '
    
    for c in data:
        try: # python 3
            dump += '{:02x} '.format(c) 
                
        except: # python 2.x
            dump += '{:02x} '.format(ord(c))
            if c >= ' ' and c < '~':
                dump_ascii += c
            else:
                dump_ascii += '.'

        if(i % 16 == 0):
            dump = dump + padding + dump_ascii + '\n\t'
            dump_ascii = ''
        i+=1
       
    if dump_ascii:
        for i in range(16 - len(dump_ascii)):
            padding += '   '
        dump = dump + padding + dump_ascii + '\n\t'

    return dump


def get_datetime():
    """
    Get current date and time (for ISO data fields)
    """
    return int(datetime.now().strftime("%d%m%H%M%S"))


def get_datetime_with_year():
    """
    Get current time (for ISO data fields)
    """
    return int(datetime.now().strftime("%y%m%d%H%M%S"))


def get_timestamp(t=None):
    """
    Get current timestamp for logging purposes
    TODO: get milliseconds
    """
    return datetime.now().strftime("%H:%M:%S.%f")


def get_stan():
    """
    Get random systems trace audit number
    """
    return random.randint(0, 999999)


def trace(title, data):
    """
    """
    print('\n{} {}\n{}'.format(get_timestamp(), title, dump(data)))


def get_response(code):
    """
    Return xx1x response for xx0x codes (e.g. 0810 for 0800)
    """
    return code[:-2] + '1' + code[-1]


def trace_passed(description):
    """
    """
    padding = ''
    for i in range(46 - len(description)):
        padding += ' '
    print("{}\t| {}{}[\033[32mPASSED\033[0m]".format(get_timestamp(), description[:46], padding))


def trace_failed(description, expected, actual_response, actual_response_description):
    """
    """
    padding = ''
    for i in range(46 - len(description)):
        padding += ' '
    print('{}\t| {}{}[\033[31mFAILED\033[0m]'.format(get_timestamp(), description[:46], padding))
