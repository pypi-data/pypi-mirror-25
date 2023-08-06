# -*- coding: utf-8 -*-
#
"""Decimal time module.

   Assumption:  We're using UTC as the default, and only, timezone.
"""

import sys
import argparse

import time
from colorama import Fore
import baseconv


def return_time_list(ts, base=10):
    """Returns array of [yy, m, w, d, h, mn, sc] in base (default 10)

    :param int ts: unix timestamp.
    :param int base: number base for output.  default 10. valid 2-64.
    """
    tl = []

    bconv = baseconv.BaseConverter(baseconv.BASE64_ALPHABET[:base])
    t = bconv.encode(ts)
    e = None
    if len(t) < 12:
        t = '0' * (10-len(t)) + t
    for i in [-2, -4, -5, -6, -7, -8]:
        tl.append(t[i:e])
        e = i
    rest = t[:-8]
    tl.append(rest)
    tl.reverse()
    return(tl)


def color_time_list(tl):
    """Wraps ansi color codes around string time values in list.

    ANSI color scheme: red, green, yellow, blue, magenta, cyan, white

    :param list tl: list of string values of time parts.
    :returns list:

    """
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA,
              Fore.CYAN, Fore.WHITE]
    l = []
    for tpl in zip(colors, tl, [Fore.RESET]*len(colors)):
        _t = list(tpl)
        l.append("".join(_t))
    return l


def time_string(ts, color=False, base=10):
    """Returns a timestring in 'yy:m:w:d h:mm:ss' format, optionally ansi color coded.

    Uses base 10 as default.
    """

    a = return_time_list(ts, base=base)
    if color:
        a = color_time_list(a)
    return(':'.join(a[:-3]) + ' ' + ':'.join(a[-3:]))


def main(argv=None):
    """main(sys.argv[1:])

    """

    parser = argparse.ArgumentParser(description='template cli script')

    parser.add_argument('--debug', default=False, action='store_true',
                        help="debug flag.")

    parser.add_argument('--ts', default=int(time.time()), action='store',
                        help="timestamp. default now().")
    parser.add_argument('--base', default=10, action='store', type=int,
                        help="base from 2-64. default 10.")
    parser.add_argument('--color', default=False, action='store_true',
                        help="colorize time positions.")

    if argv is not None:
        args = parser.parse_args(argv)
    else:
        args = parser.parse_args()

    a = time_string(args.ts, color=args.color, base=args.base)
    print(a)


if __name__ == '__main__':
    main(sys.argv[1:])
