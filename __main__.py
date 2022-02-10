#!/usr/bin/env python3

import argparse

from . import file_ops
from .Generator import Generator


def main():
    args = handle_arguments()

    if args.input is None or args.output is None:
        raise Exception('Check --help for usage')

    descriptor = file_ops.read_yaml_file(args.input)
    generator = Generator(descriptor, debug_level=args.debug)
    generator.generate_table()
    file_ops.write_csv_file(args.output, generator.get_table())


def handle_arguments():
    parser = argparse.ArgumentParser(description='This script can generate a random table by defined rules')
    parser.add_argument('-i', '--input', help='input file (yaml)')
    parser.add_argument('-o', '--output', help='output file (cvs)')
    parser.add_argument('-d', '--debug', help='debug level', default=0, type=positive_integer)

    return parser.parse_args()


def positive_integer(astring):
    if int(astring) < 0:
        raise ValueError

    return int(astring)


if __name__ == "__main__":
    main()
