# -*- coding: utf-8 -*-
# :Project:   pg_query -- Simple frontend to the pretty reformatter
# :Created:   dom 06 ago 2017 23:09:23 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Lele Gaifax
#

import argparse
import json
import sys

from pg_query import Error, parse_sql, prettify


def workhorse(args):
    input = args.infile or sys.stdin
    with input:
        statement = input.read()

    if args.parse_tree:
        tree = parse_sql(statement)
        output = args.outfile or sys.stdout
        with output:
            json.dump(tree, output, sort_keys=True, indent=2)
            output.write('\n')
    else:
        try:
            prettified = prettify(statement, compact_lists_margin=args.compact_lists_margin)
        except Error as e:
            print()
            raise SystemExit(e)

        output = args.outfile or sys.stdout
        with output:
            output.write(prettified)
            output.write('\n')


def main(options):
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(description="PostgreSQL language prettifier",
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-t', '--parse-tree', action='store_true', default=False,
                        help='show just the parse tree of the statement')
    parser.add_argument('-m', '--compact-lists-margin', type=int, default=0,
                        help='use compact form for lists not exceeding the given margin')
    parser.add_argument('infile', nargs='?', type=argparse.FileType(),
                        help='a file containing the SQL statement to be pretty-printed,'
                       ' by default stdin')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        help='where the result will be written, by default stdout')

    args = parser.parse_args(options)

    workhorse(args)


if __name__ == '__main__': #pragma: no cover
    main(sys.argv[1:])
