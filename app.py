#!/usr/bin/env python3

import argparse

from flights import io, engine


arg_parser = argparse.ArgumentParser(
    description='Delays predictor',
)
arg_parser.add_argument('--redis', action='store_true',
                        help='Try to use Redis as much as possible.')
arg_parser.add_argument('--import', dest='import_csv', metavar='CSV',
                        help='Imports content of a CSV file.')
arg_parser.add_argument('--sparse', type=int, metavar='INT',
                        help='Optional sparseness for import.')
arg_parser.add_argument('--predict', action='store_true',
                        help='Predicts departures.')
arg_parser.add_argument(
    '--diff',
    action='store_true',
    help='Computes sum(abs(predicted_departure - actual_departure)).',
)
arg_parser.add_argument('--export', dest='export_csv', metavar='CSV',
                        help='Exports flights to a CSV file.')


def main():
    args = arg_parser.parse_args()

    if args.import_csv:
        io.import_csv(open(args.import_csv),
                      save=io.save_redis if args.redis
                           else io.save_db,
                      sparse=args.sparse)

    if args.predict:
        if args.redis:
            engine.predict_redis()
        else:
            engine.predict_db()

    if args.diff:
        diff = engine.compute_diff_redis() if args.redis \
               else engine.compute_diff_db()
        print('sum: %(sum)s\ncount: %(count)d\navg: %(avg)s' % diff)

    if args.export_csv:
        io.export_csv(open(args.export_csv, 'w'),
                      load=io.load_redis if args.redis
                           else io.load_db)


if __name__ == '__main__':
    main()
