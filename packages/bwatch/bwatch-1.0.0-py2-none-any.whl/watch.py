"""A Binary Watch Presentation"""
from __future__ import print_function
import sys
import time

__version__ = '1.0.0'
__author__ = 'hellflame'
__url__ = 'https://github.com/hellflame/binary_clock/tree/v' + __version__


if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

COLORS = ['\033[01;34m{}\033[00m', '\033[01;34m{}\033[00m',  # Month
          '\033[01;35m{}\033[00m', '\033[01;35m{}\033[00m',  # Day
          '\033[01;31m{}\033[00m',                           # Week
          '\033[01;36m{}\033[00m', '\033[01;36m{}\033[00m',  # Hour
          '\033[01;32m{}\033[00m', '\033[01;32m{}\033[00m',  # Min
          '\033[01;33m{}\033[00m', '\033[01;33m{}\033[00m']  # Sec
THEMES = {
    'raw': None,
    'smallBox': (u'\u25A1', u'\u25A0'),
    'bigBox': (u'\u25A2', u'\u25A9'),
    'boxSimple': ('-', u'\u25A3'),
    'circleSimple': ('-', u'\u25C9'),
    'rhombusSimple': ('-', u'\u25C8')
}


def to_matrix(n):
    """
    convert decimal to binary matrix, at most 4 bits deep ( because 9 < 15 )
    `numpy` seems not always available, or it will be much easy to do so
    :param n: str (decimal int value)
    :return: list
    """
    tmp = ['{:0>4}'.format("{:b}".format(int(s))) for s in n]
    return [[tmp[index][i] for index in range(len(tmp))] for i in range(4)]


def theme_print(theme, text, color=False):
    if color:
        if len(text[0]) == 11:
            for line in text:
                if THEMES.get(theme):
                    print(" ".join([COLORS[i].format(THEMES[theme][int(x)]) for i, x in enumerate(line)]))
                else:
                    print(" ".join([COLORS[i] for i, x in enumerate(line)]))
        else:
            for line in text:
                if THEMES.get(theme):
                    print(" ".join([COLORS[i + 5].format(THEMES[theme][int(x)]) for i, x in enumerate(line)]))
                else:
                    print(" ".join([COLORS[i + 5].format(x) for i, x in enumerate(line)]))
    else:
        for line in text:
            if THEMES.get(theme):
                print(" ".join([THEMES[theme][int(x)] for x in line]))
            else:
                print(" ".join(line))


def glimpse(theme='boxSimple', full=False, hint=False, color=False):
    t = time.localtime()
    if theme == 'basic':
        # Not So Pretty
        if full:
            if hint:
                print("{} | Month : {:>2}".format((" " * 7).join("{:b}".format(t.tm_mon).rjust(4)), t.tm_mon))
                print("{} |   Day : {:>2}".format((" " * 5).join("{:b}".format(t.tm_mday).rjust(5)), t.tm_mday))
                print("{} |  Week : {:>2}".format((" " * 7).join("{:b}".format(t.tm_wday + 1).rjust(4)),
                                                  t.tm_wday + 1))
            else:
                print("{}".format((" " * 7).join("{:b}".format(t.tm_mon).rjust(4))))
                print("{}".format((" " * 5).join("{:b}".format(t.tm_mday).rjust(5))))
                print("{}".format((" " * 7).join("{:b}".format(t.tm_wday + 1).rjust(4))))
        if hint:
            print("{} |  Hour : {:>2}".format((" " * 5).join('{:b}'.format(t.tm_hour).rjust(5)), t.tm_hour))
            print("  {}   |   Min : {:>2}".format((" " * 3).join('{:b}'.format(t.tm_min).rjust(6)), t.tm_min))
            print("  {}   |   Sec : {:>2}".format((" " * 3).join('{:b}'.format(t.tm_sec).rjust(6)), t.tm_sec))
        else:
            print("{}".format((" " * 5).join('{:b}'.format(t.tm_hour).rjust(5))))
            print("  {}   ".format((" " * 3).join('{:b}'.format(t.tm_min).rjust(6))))
            print("  {}   ".format((" " * 3).join('{:b}'.format(t.tm_sec).rjust(6))))
    elif theme in THEMES:
        # Kinda
        if full:
            raw = '{month:0>2}{day:0>2}{week}{hour:0>2}{min:0>2}{sec:0>2}'.format(month=t.tm_mon,
                                                                                  day=t.tm_mday,
                                                                                  week=t.tm_wday + 1,
                                                                                  hour=t.tm_hour,
                                                                                  min=t.tm_min,
                                                                                  sec=t.tm_sec)
            result = to_matrix(raw)
            if hint:
                theme_print(theme, result, color)
                print("_" * 21)
                print('M M D D W h h m m s s')
                print(' '.join(raw))
            else:
                theme_print(theme, result, color)
        else:
            raw = '{hour:0>2}{min:0>2}{sec:0>2}'.format(hour=t.tm_hour, min=t.tm_min, sec=t.tm_sec)
            result = to_matrix(raw)
            if hint:
                theme_print(theme, result, color)
                print("_" * 11)
                print('h h m m s s')
                print(' '.join(raw))
            else:
                theme_print(theme, result, color)


def loop_watch(theme='basic', full=True, hint=True, color=False):
    """
    start watch click, control-C to stop
    :param theme: print style choice
    :param full: set True to print full length date time string
    :param hint: set True to print human-readable date time or else, programmer-readable date time
    :param color: set True to print colorful columns, more easy to read

    :type theme: String
    :type full: Boolean
    :type hint: Boolean
    :type color: Boolean
    :return: None
    """
    try:
        while True:
            glimpse(theme, full, hint, color)
            if theme == 'basic':
                if full:
                    sys.stdout.write("\033[F" * 6)
                else:
                    sys.stdout.write("\033[F" * 3)
            elif theme in THEMES:
                if hint:
                    sys.stdout.write("\033[F" * 7)
                else:
                    sys.stdout.write("\033[F" * 4)
            time.sleep(.05)
    except KeyboardInterrupt:
        if theme == 'basic':
            if full:
                sys.stdout.write("\n" * 6)
            else:
                sys.stdout.write("\n" * 3)
        elif theme in THEMES:
            if hint:
                sys.stdout.write("\n" * 7)
            else:
                sys.stdout.write("\n" * 4)


def terminal():
    import argparse

    def available_themes(s):
        if s not in THEMES and not s == 'basic':
            raise argparse.ArgumentTypeError("`{}` is not a supported theme.\n`basic / {}` are available".format(s, " / ".join(THEMES.keys())))
        return s

    parser = argparse.ArgumentParser(description=__doc__,
                                     version=__version__,
                                     epilog="More Info, visit " + __url__)
    parser.add_argument('--hint', action="store_true", help="show easy read time outputs")
    parser.add_argument('-nc', '--no-color', action='store_true', help="supress color output")
    parser.add_argument('-g', '--glimpse', action="store_true", help="show only one moment time")
    parser.add_argument('-f', '--full', action="store_true", help="output Month, Day, Week")
    parser.add_argument('-t', '--theme', default="boxSimple", type=available_themes,
                        help="choose output theme, default `boxSimple`.")

    args = parser.parse_args()
    if args.glimpse:
        glimpse(args.theme, full=args.full, hint=args.hint, color=not args.no_color)
    else:
        loop_watch(args.theme, full=args.full, hint=args.hint, color=not args.no_color)


if __name__ == '__main__':
    terminal()
    # loop_watch('smallBox', hint=False, full=False, color=True)
