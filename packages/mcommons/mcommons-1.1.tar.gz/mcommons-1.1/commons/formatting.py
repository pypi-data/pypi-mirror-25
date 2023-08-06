from colorama import init
import pytz
import dateutil.parser

from terminal import *

MB = 1024 * 1024
GB = MB * 1024
TB = GB * 1024
K = 1000
M = K * 1000


def format_unit(amount, divisor, unit):
    if amount % divisor == 0:
        return '{0:.0f}{1}'.format(float(amount)/divisor, unit)
    return '{0:.2f}{1}'.format(float(amount)/divisor, unit)


def format_bytes(bytes):
    try:
        bytes = float(bytes)
    except:
        return bytes

    if bytes is None or bytes is 0:
        return ""

    if bytes >= TB:
        return format_unit(bytes, TB, 'TB')
    if bytes >= GB:
        return format_unit(bytes, GB, 'GB')
    return format_unit(bytes, MB, 'MB')


def format_num(space):
    if space is None or space is 0:
        return ""
    if space >= M:
        return '{0:.1f}m'.format(float(space) / M)
    elif space >= K:
        return '{0:.1f}k'.format(float(space)/ K)
    return int(space)


def get_age_in_seconds(date):
    import datetime as dt
    try:
        diff = pytz.utc.localize(dt.datetime.now()) - dateutil.parser.parse(date)
        return diff.days * 24 * 60 * 60 + diff.seconds
    except Exception, e:
        return str(e)


def format_seconds(seconds):
    if seconds is None or seconds == "":
        return ""
    try:
        seconds = float(seconds)
        fmt = "{0:.0f} {1}"
        if seconds < 60:
            return fmt.format(seconds, "s")
        elif seconds < 60 * 60:
            return fmt.format(seconds / 60, "m")
        elif seconds < 60 * 60 * 24:
            return fmt.format(seconds / 60 / 60, "h")
        else:
            return fmt.format(seconds / 60 / 60 / 24, "d")
    except Exception, e:
        return str(e) + str(seconds)


def format_mem(mem):
    if mem is None:
        return ""
    return '{0:.2f}GB'.format(float(mem)/1024)


def format_space(space):
    return format_bytes(space)


def get_colored_percent(percentage, factor=1):
    if percentage > 90 / factor:
        percentage = red("%.0f%%" % percentage)
    elif percentage > 70 / factor:
        percentage = yellow("%.0f%%" % percentage)
    else:
        percentage = green("%.0f%%" % percentage)
    return "@ %s" % (percentage)




