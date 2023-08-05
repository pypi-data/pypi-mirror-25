"""A Binary Watch Presentation"""
from __future__ import print_function
import sys
import time

__version__ = '1.0.1'
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
    'boxBlank': (' ', u'\u25A3'),
    'circleSimple': ('-', u'\u25C9'),
    'circleBlank': (' ', u'\u25C9'),
    'rhombusSimple': ('-', u'\u25C8'),
    'rhombusBlank': (' ', u'\u25C8'),
    'plusSimple': ('-', '+'),
    'plusBlank': (' ', '+')
}


def transpose(n):
    """
    convert decimal to binary matrix (transposition), at most 4 bits deep ( because 9 < 15 )
    `numpy` seems not always available, or it will be much easier to do so using `numpy.concatenate`

    progress like:
        n => bin(n) => [[0, 1, ...], [1, 1, ...], [1, 0, ...], [0, 0, ... ]]
    eg:
        n = '17'
    =>  ['0001', '0111'] 
    =>  [[0, 0], [0, 1], [0, 1], [1, 1]]

    if print in the console, it may look like this:
    from:
        0 0 0 1
        0 1 1 1
    to:
        0 0
        0 1
        0 1
        1 1

    :param n: str (decimal int value)
    :return: list of 4 lists
    """
    tmp = ['{:0>4}'.format("{:b}".format(int(s))) for s in n]
    return [[tmp[index][i] for index in range(len(tmp))] for i in range(4)]


def theme_print(theme, text, color=False):
    """
    print transposed text in the console

    :param theme: str
    :param text: list of 4 lists
    :param color: bool
    :return: None
    """
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
    """
    show a glimpse of localtime

    :param theme: str
    :param full: bool
    :param hint: bool
    :param color: bool
    :return: None
    """
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
            result = transpose(raw)
            if hint:
                theme_print(theme, result, color)
                print("_" * 21)
                print('M M D D W h h m m s s')
                print(' '.join(raw))
            else:
                theme_print(theme, result, color)
        else:
            raw = '{hour:0>2}{min:0>2}{sec:0>2}'.format(hour=t.tm_hour, min=t.tm_min, sec=t.tm_sec)
            result = transpose(raw)
            if hint:
                theme_print(theme, result, color)
                print("_" * 11)
                print('h h m m s s')
                print(' '.join(raw))
            else:
                theme_print(theme, result, color)


def loop_watch(theme='basic', full=True, hint=True, color=False):
    """
    start watch click, control-C to stop, 
    this basically just keep calling `glimpse` 

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
        #  Control-C pressed
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
    """
    command line entry
    """
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
    if True:
        # default to unit test
        import unittest
        import random

        class TransTest(unittest.TestCase):
            """transpose test cases"""
            def random_gen(self, length):
                target = ''.join([random.choice('0123456789') for _ in range(length)])
                rand_choice = random.choice(range(length))

                self.assertListEqual(list('{:0>4}'.format('{:b}'.format(int(target[rand_choice])))),
                                     [transpose(target)[i][rand_choice] for i in range(4)])

            def test_simple(self):
                self.assertListEqual([['0', '0'], ['0', '1'], ['0', '1'], ['1', '1']], transpose('17'))

            def test_complex(self):
                self.random_gen(1)
                self.random_gen(3)
                self.random_gen(50)
                self.random_gen(100)
                self.random_gen(200)

            def test_empty(self):
                self.assertListEqual([[], [], [], []], transpose(''))

            def test_very_long(self):
                self.random_gen(2 ** 20)

            def test_keep_always(self):
                target = ''.join([random.choice('0123456789') for _ in range(100)])
                self.assertListEqual(transpose(target),
                                     transpose(target))
            
            def test_level1_depth(self):
                self.assertEqual(len(transpose(''.join([random.choice('0123456789')
                                                        for _ in range(100)]))),
                                 4)

            def test_level2_depth(self):
                self.assertEqual(len(transpose(''.join([random.choice('0123456789')
                                                        for _ in range(100)]))[0]),
                                 100)

        unittest.main()
    else:
        terminal()
    # loop_watch('smallBox', hint=False, full=False, color=True)









