# -*- coding: utf-8 -*-

import sys
import os
import argparse
import configparser

from reverpf import __version__

def build_parser():
    """ Parser args """
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--format', type=str,
                        dest='fmt', default=None, metavar='FORMAT',
                        help='Format from printf')

    parser.add_argument('-i', '--input-file', type=str,
                        dest='file', default=None, metavar='FILE',
                        help='File input')

    parser.add_argument('-a', '--alias-format', type=str,
                        dest='alias', default=None, metavar='ALIAS',
                        help='Alias format from config file')

    parser.add_argument('-s', '--separator', type=str,
                        dest='sep', default=None, metavar='SEPARATOR',
                        help='Separator string')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    return parser


def config_parser():
    """ Config parser to dict """

    cfgfile = os.path.join(os.path.expanduser("~"), '.reverpfrc')
    alias = {}

    if os.path.isfile(cfgfile):

        with open(cfgfile, 'r') as f:
            config_string = '[dummy_section]\n' + f.read()
        config = configparser.RawConfigParser()
        config.read_string(config_string)

        for name, value in config.items('dummy_section'):
            alias[name] = value

    return alias


def _get_sep_positions(s, sep):
    pos = [i for i in range(len(s)) if s.startswith(sep, i)]

    new_pos = []
    correct = 0

    for i in pos:
        new_pos.append(i - correct)
        correct += len(sep)

    return new_pos


def _cut_by_positions(s, positions, sep='|'):
    n = []
    i = 0
    for j in positions:
        n.append(s[i:j])
        i = j

    n.append(s[i:])

    return sep.join(n) + sep


def rever_printf(fmt, line, sep='|'):

    fmt_sep = fmt.replace('%', '|%')
    count = fmt.count('%')

    # obtenemos la línea tal como sería pero con 1's
    s_zero = fmt_sep % tuple([1] * count)

    positions = _get_sep_positions(s_zero, '|')

    return _cut_by_positions(line, positions, sep)


def rever(input_file, fmt, sep):
    if not input_file:
        finput = sys.stdin
    else:
        finput = open(input_file)

    if not sep:
        sep = ';'

    with finput as f:
        for line in f:
            line = line.strip('\n')
            try:
                rline = rever_printf(fmt, line, sep)
                print(rline)
            except Exception as e:
                print("Error '{0}' occured.".format(e.message))
                print('error: format or data error', file=sys.stderr)
                sys.exit(2)


def main():

    parser = build_parser()
    options = parser.parse_args()
    configs = config_parser()

    # opciones excluyentes...
    if options.alias and options.fmt or not options.alias and not options.fmt:
        parser.print_help()
        print("""\nerror: --format and --alias are mutually exclusive and"""
              """ one necesary""")
        sys.exit(2)

    if options.alias:
        if options.alias in configs:
            fmt = configs[options.alias]
        else:
            print('error: alias not found in .reverpfrc or file not exists')
            sys.exit(2)
    else:
        fmt = options.fmt

    rever(options.file, fmt, options.sep)


if __name__ == '__main__':
    main()
