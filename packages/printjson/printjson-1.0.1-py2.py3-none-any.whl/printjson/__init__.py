#!/usr/bin/env python3

import json
import argparse
import sys
import os.path
import os


COLOR_PREAMBLE = '\x1b[38;5;'
COLORS_16 = [str(i) + 'm' for i in range(0, 16)]
COLOR_0 = '0m'

# C_RES = COLOR_PREAMBLE + COLOR_0
C_RES = '\x1b[0m'
C_DIC = COLOR_PREAMBLE + COLORS_16[14]
C_LST = COLOR_PREAMBLE + COLORS_16[12]
C_NUM = COLOR_PREAMBLE + COLORS_16[9]
C_NUL = COLOR_PREAMBLE + COLORS_16[11]
C_STR = COLOR_PREAMBLE + COLORS_16[2]


class Main:

    def __init__(self, path, print_errors, key_str, delimiter):
        self.path = path
        self.print_errors = print_errors
        self.delimiter = delimiter
        self.key_str = key_str

    def print_error(self, file, args=None, line=0, column=0, msg='', doc=''):
        """Print JSON error message"""
        if args is None:
            errorstr = 'JSON incorrect!\nLine: %d\nColumn: %d\n\n%s\n%s\n' % (line, column, msg, doc)
        else:
            errorstr = 'JSON incorrect!\n\n' + args[0] + '\n' + doc
        sys.stderr.write(errorstr)

    def parse_key(self):
        """Parse key sequence to extract data from JSON"""
        if self.key_str is None:
            return list()
        else:
            return self.key_str.split(self.delimiter)

    def extract_key(self, data, key_seq):
        """Extract data by key chain from JSON"""
        for i in key_seq:
            try:
                if isinstance(data, list) or isinstance(data, tuple):
                    data = data[int(i)]
                else:
                    data = data[i]
            except KeyError:
                if self.print_errors:
                    sys.stderr.write("Error: No key '%s' in file %s\n" % (i, self.path))
                sys.exit(5)
            except TypeError:
                if self.print_errors:
                    sys.stderr.write("Error: Incorrect index '%s' in file %s\n" % (i, self.path))
                sys.exit(6)
        return data

    def load_json(self):
        """Loadf and check JSON file"""
        if not os.path.isfile(self.path):
            if self.print_errors:
                sys.stderr.write("Error: File %s not found\n" % self.path)
            sys.exit(3)
        try:
            file = open(self.path)
        except Exception:
            if self.print_errors:
                sys.stderr.write("Error: Couldn't open %s\n" % self.path)
            sys.exit(4)
        try:
            data = json.load(file)
        except Exception as e:
            if self.print_errors:
                if hasattr(e, 'lineno') and hasattr(e, 'colno') and hasattr(e, 'msg') and hasattr(e, 'doc'):
                    self.print_error(file, None, e.lineno, e.colno, e.msg, e.doc)
                elif hasattr(e, 'args'):
                    self.print_error(file, e.args)
            sys.exit(1)
        return data

    def get_data(self):
        """Get data from loaded dict"""
        return self.extract_key(self.load_json(), self.parse_key())



class PrinterJSON:
    """Print data structure as JSON"""
    c_lst = 13
    c_dic = 12
    c_dat = 15
    c_log = 11
    c_key = 2
    c_val = 3
    color = True
    minimize = False
    sep1 = ': '
    sep2 = ',\n'
    termdic = ('{\n', '\n}')
    termlst = ('[\n', '\n]')
    curind = 0
    ind = 2
    onkey = True

    def __init__(self, color=True, minimize=False):
        self.color = color
        self.set_minimize(minimize)
        self.simple_data = None

    def set_minimize(self, mode=None):
        """Set separators for minimization"""
        if mode is not None:
            self.minimize = mode
        if self.minimize:
            self.termdic = ('{', '}')
            self.termlst = ('[', ']')
            self.sep1 = ':'
            self.sep2 = ','
            self.ind = 0
        else:
            self.termdic = ('{\n', '\n}')
            self.termlst = ('[\n', '\n]')
            self.sep1 = ': '
            self.sep2 = ',\n'
            self.ind = 2

    def set_color(self, num):
        """Set output color of stdout to num"""
        if self.color:
            if 0 < num < len(COLORS_16):
                sys.stdout.write(COLOR_PREAMBLE + COLORS_16[num])
            else:
                sys.stdout.write(C_RES)

    def reset_color(self):
        """Set output color of stdout to default"""
        if self.color:
            sys.stdout.write(C_RES)

    def cpr(self, string, color_num):
        """Print colorized string"""
        self.set_color(color_num)
        sys.stdout.write(string)
        self.reset_color()

    def print_indent(self):
        sys.stdout.write(' ' * self.curind)

    def end(self, p, c):
        self.cpr(p.replace('\n', '\n' + ' ' * self.curind), c)

    def print_bool(self, a):
        """Print bool or null variable"""
        self.set_color(self.c_log)
        if a is True:
            sys.stdout.write('true')
        elif a is False:
            sys.stdout.write('false')
        elif a is None:
            sys.stdout.write('null')
        self.reset_color()

    def print_num(self, a):
        """Print number."""
        self.cpr(str(a), self.c_dat)

    def print_str(self, a):
        """Print string with colorized (if set) brackets"""
        if not self.simple_data:
            if self.onkey:
                self.cpr('"', self.c_key)
            else:
                self.cpr('"', self.c_val)
        sys.stdout.write(a)
        if not self.simple_data:
            if self.onkey:
                self.cpr('"', self.c_key)
            else:
                self.cpr('"', self.c_val)

    def print_list(self, a):
        """Print list, colorized if set"""
        self.cpr(self.termlst[0], self.c_lst)
        self.curind += self.ind
        for i in range(len(a)):
            self.print_indent()
            self.print_data(a[i])
            if i < len(a) - 1:
                self.cpr(self.sep2, self.c_lst)
        self.curind -= self.ind
        self.end(self.termlst[1], self.c_lst)

    def print_dict(self, a):
        """Print dictionary, colorized if set"""
        self.cpr(self.termdic[0], self.c_dic)
        self.curind += self.ind
        it = [i for i in a.items()]
        for i in range(len(it)):
            self.print_indent()
            self.onkey = True
            self.print_str(str(it[i][0]))
            self.cpr(self.sep1, self.c_dic)
            self.onkey = False
            self.print_data(it[i][1])
            if i < len(it) - 1:
                self.cpr(self.sep2, self.c_dic)
        self.curind -= self.ind
        self.end(self.termdic[1], self.c_dic)

    def start_print_data(self, data):
        """Check if data not list or dictionary and prints it"""
        if isinstance(data, dict) or isinstance(data, list):
            self.simple_data = False
        else:
            self.simple_data = True
        self.print_data(data)

    def print_data(self, data):
        """Print data for JSON"""
        if isinstance(data, dict):
            self.print_dict(data)
        elif isinstance(data, list):
            self.print_list(data)
        elif isinstance(data, bool) or data is None:
            self.print_bool(data)
        elif isinstance(data, int) or isinstance(data, float):
            self.print_num(data)
        else:
            self.print_str(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to JSON file')
    parser.add_argument('-o', '--one-color', help='disable color sequences in output', action="store_true",  default=0)
    parser.add_argument('-m', '--minimize', help='minimize JSON', action="store_true", default=0)
    parser.add_argument('-s', '--sort', help='sort by keys', action="store_true", default=0)
    parser.add_argument('-q', '--quiet', help='print nothing for check correctness', action="store_true", default=0)
    parser.add_argument('-n', '--no-errors', help='print no errors', action="store_true", default=0)
    parser.add_argument('-e', '--errors-only', help='print only errors', action="store_true", default=0)
    parser.add_argument('-k', '--key', help='key to output, example: -k exmp..exmp..4..exmp', type=str)
    parser.add_argument('-d', '--delimiter', help='delimiter for key sequence, example: -d ".."', type=str, default='.')
    args = parser.parse_args()
    wrk = Main(args.path, not args.no_errors and not args.quiet, args.key, args.delimiter)
    data = wrk.get_data()
    if not args.errors_only and not args.quiet:
        printer = PrinterJSON(color=(not args.one_color and sys.stdout.isatty()), minimize=args.minimize)
        printer.start_print_data(data)
        sys.stdout.write('\n')
