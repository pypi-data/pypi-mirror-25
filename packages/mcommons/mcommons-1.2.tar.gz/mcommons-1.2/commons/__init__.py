
import socket
import time
import os
import datetime as dt
import threading
import ssl
import sys


from terminal import *
from formatting import *
from net import *
from shell import *
from Table import *
from crypto import *

from tempfile import mkstemp


class Timer:

    def __init__(self):
        self.start = dt.datetime.now()

    def __str__(self):
        return str(dt.datetime.now() - self.start)

    def __repr__(self):
        return str(dt.datetime.now() - self.start)


def call_async(func, args):
    t = threading.Thread(target=func, args=args)
    t.daemon = True
    t.start()

    def null():
        pass

    return null

def async(func, args):
    t = threading.Thread(target=func, args=args)
    t.daemon = True
    t.start()

    def null(args):
        pass

    return null

def read(path):
    with open(path, 'r') as f:
        return f.read()

def write(path, str):
    with open(path, 'w') as f:
        f.write(str)

def wait(condition, sleep=1):
    result = condition()
    while result is False:
        result = condition()
        time.sleep(sleep)
