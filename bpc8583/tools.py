import random

from time import strftime
from math import pow
from datetime import datetime
from tracetools.tracetools import get_timestamp
from pynblock.tools import hexify


def get_date():
    """
    Get current date YYMMDD
    """
    return datetime.now().strftime("%y%m%d")


def get_MMDD():
    """
    Get current date MMDD
    """
    return int(datetime.now().strftime("%m%d"))


def get_datetime():
    """
    Get current date and time (for ISO data fields)
    """
    return int(datetime.now().strftime("%d%m%H%M%S"))


def get_time():
    """
    Get current timestamp (for ISO data fields)
    """
    return int(datetime.now().strftime("%H%M%S"))


def get_datetime_with_year():
    """
    Get current time (for ISO data fields)
    """
    return int(datetime.now().strftime("%y%m%d%H%M%S"))


def get_seconds_since_epoch():
    """
    Get number of seconds since Jan 01 1970
    """
    return int((datetime.now()-datetime(1970,1,1)).total_seconds())


def get_stan():
    """
    Get random systems trace audit number
    """
    return random.randint(0, 999999)


def get_random_hex(length):
    """
    Return random hex string of a given length
    """
    if length <= 0:
        return ''
    return hexify(random.randint(pow(2, length*2), pow(2, length*4)))[0:length]


def get_response(_code):
    """
    Return xx1x response for xx0x codes (e.g. 0810 for 0800)
    """
    if _code:
        code = str(_code)
        return code[:-2] + str(int(code[-2:-1]) + 1) + code[-1]
    else:
        return None


def trace_passed(description, show_colored_description=False):
    """
    """
    padding = ''
    for i in range(56 - len(description)):
        padding += ' '
    if show_colored_description:
        print("{}\t| \033[32m{}\033[0m{}[\033[32mPASSED\033[0m]".format(get_timestamp(), description[:56], padding))
    else:
        print("{}\t| {}{}[\033[32mPASSED\033[0m]".format(get_timestamp(), description[:56], padding))


def trace_failed(description, actual_response, show_colored_description=False):
    """
    """
    padding = ''
    for i in range(56 - len(description)):
        padding += ' '
    if show_colored_description:
        print('{}\t| \033[31m{}\033[0m{}[\033[31mFAILED\033[0m]'.format(get_timestamp(), description[:56], padding))
    else:
        print('{}\t| {}{}[\033[31mFAILED\033[0m]'.format(get_timestamp(), description[:56], padding))
