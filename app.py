#!/usr/bin/env python3

import argparse

from flights import io, models


arg_parser = argparse.ArgumentParser(
    description='Delays predicator',
)
arg_parser.add_argument('--create', action='store_true',
                        help='Creates DB schema.')
arg_parser.add_argument('--import-db', dest='import2db', metavar='CSV',
                        help='Imports content of a CSV file into DB.')
arg_parser.add_argument('--import-redis', dest='import2redis', metavar='CSV',
                        help='Imports content of a CSV file into Redis.')


def main():
    args = arg_parser.parse_args()

    if args.create:
        models.create_db()

    if args.import2db:
        io.import_csv(open(args.import2db), save=io.save_db)

    if args.import2redis:
        io.import_csv(open(args.import2redis), save=io.save_redis)


if __name__ == '__main__':
    main()
