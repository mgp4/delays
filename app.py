#!/usr/bin/env python3

import argparse

from flights.models import create_db
from flights.parser import parse_csv


arg_parser = argparse.ArgumentParser(
    description='Delays predicator',
)
arg_parser.add_argument('--create', action='store_true',
                        help='Creates DB schema.')
arg_parser.add_argument('--import', dest='import_file', metavar='CSV',
                        help='Imports content of a CSV file into DB.')


def main():
    args = arg_parser.parse_args()

    if args.create:
        create_db()

    if args.import_file:
        parse_csv(open(args.import_file))


if __name__ == '__main__':
    main()
