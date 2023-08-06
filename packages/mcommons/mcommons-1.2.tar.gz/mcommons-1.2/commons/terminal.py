from colorama import init
init()  # make ansi terminal codes work on win32
from colors import black, green, red, yellow, blue, magenta, cyan, white, color
import sys

CLEAR_SCREEN="\x1b[2J\x1b[H"
ERASE_LINE = '\x1b[2K \r'


def white(s):
    return s


def orange(s):
    return color(s, fg=3)


def gray(msg):
    return color(msg, fg=242)


def red(msg):
    return color(msg, fg=196)

CROSS = red(u'\u2717')
TICK = green(u'\u2714')

def update_title(title):
    sys.stderr.write("\033]0;%s\007" % title)

def move_cursor(x,y):
    return u"\u001b[%s;%sH" % (x,y)

def print_info(str):
    sys.stderr.write(magenta(str))
    return magenta(str)

def print_msg(str):
    sys.stderr.write(str)
    return str

def print_ok(str):
    sys.stderr.write(green(str))
    return green(str)

def print_fail(str):
    sys.stderr.write(red(str.split("\n")[0]))
    return red(str)

def update_line(line):
    sys.stderr.write(ERASE_LINE + line + "\033[K")
    sys.stderr.flush()
    return line