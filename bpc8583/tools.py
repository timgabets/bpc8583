import random

from time import strftime
from math import pow
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
            
        if chr(c) >= ' ' and chr(c) < '~':
            dump_ascii += chr(c)
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


def get_date():
    """
    Get current date
    """
    return datetime.now().strftime("%y%m%d")



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
    """
    return datetime.now().strftime("%H:%M:%S.%f")


def get_stan():
    """
    Get random systems trace audit number
    """
    return random.randint(0, 999999)


def hexify(number):
    """
    Convert integer to hex string representation, e.g. 12 to '0C'
    """
    if number < 0:
        raise ValueError('Invalid number to hexify - must be positive')

    result = hex(int(number)).replace('0x', '').upper()
    if divmod(len(result), 2)[1] == 1:
        # Padding
        result = '0{}'.format(result)
    return result


def get_random_hex(length):
    """
    Return random hex string of a given length
    """
    if length <= 0:
        return ''
    return hexify(random.randint(pow(2, length*2), pow(2, length*4)))[0:length]


def trace(title, data):
    """
    """
    print('{} {}\n{}\n'.format(get_timestamp(), title, dump(data)))


def get_response(_code):
    """
    Return xx1x response for xx0x codes (e.g. 0810 for 0800)
    """
    if _code:
        code = str(_code)
        return code[:-2] + '1' + code[-1]
    else:
        return None


def trace_passed(description, show_colored_description=False):
    """
    """
    padding = ''
    for i in range(46 - len(description)):
        padding += ' '
    if show_colored_description:
        print("{}\t| \033[32m{}\033[0m{}[\033[32mPASSED\033[0m]".format(get_timestamp(), description[:46], padding))
    else:
        print("{}\t| {}{}[\033[32mPASSED\033[0m]".format(get_timestamp(), description[:46], padding))


def trace_failed(description, actual_response, show_colored_description=False):
    """
    """
    padding = ''
    for i in range(46 - len(description)):
        padding += ' '
    if show_colored_description:
        print('{}\t| \033[31m{}\033[0m{}[\033[31mFAILED\033[0m]'.format(get_timestamp(), description[:46], padding))
    else:
        print('{}\t| {}{}[\033[31mFAILED\033[0m]'.format(get_timestamp(), description[:46], padding))
