import csv
import random

import dateutil.parser
import logging

from . import models, redis
from .database import db_session


logger = logging.getLogger(__name__)


def save_db(flight):
    db_session.add(models.Flight(**flight))
    db_session.commit()


def save_redis(flight):
    redis.set('flight_%s_%s' % (flight['flight_number'],
                                flight['scheduled_departure']),
              flight)


def import_csv(csvfile, save=save_db, sparse=False):
    """Imports data from CSV file.

    :param csvfile: opened file
    :param save: saving method, `save_db` or `save_redis`
    :param sparse: degree of sparseness, the greater the sparser
    """

    reader = csv.DictReader(csvfile)
    processed = 0
    imported = 0

    for row in reader:
        if processed % 1000 == 0:
            if sparse:
                logger.info('%d flights processed, %d imported...'
                            % (processed, imported))
            else:
                logger.info('%d flights imported...' % imported)

        if sparse and random.randint(0, sparse) != 0:
            processed += 1
            continue

        flight = {
            'carrier': row['carrier'],
            'flight_number': row['fltno'],
            'departure_airport': row['dep_apt'],
            'arrival_airport': row['arr_apt'],
            'scheduled_departure':
                dateutil.parser.parse(row['scheduled_departure']),
            'actual_departure':
                dateutil.parser.parse(row['actual_departure'])
                if row['actual_departure'] else None,
        }
        save(flight)

        processed += 1
        imported += 1

    logger.info('%d flights imported.' % imported)


def load_db():
    return models.Flight.query.all()


def load_redis():
    for key in redis.cache.scan_iter('flight_*'):
        yield redis.get(key)


def export_csv(csvfile, load=load_db):
    fieldnames = ['carrier', 'fltno', 'dep_apt', 'arr_apt',
                  # 'sched_departure_date',
                  'scheduled_departure', 'actual_departure']
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()

    for flight_data in load():
        col = (lambda name:
            flight_data[name] if isinstance(flight_data, dict)
                              and name in flight_data
            else getattr(flight_data, name, None)
        )
        flight = {
            'carrier': col('carrier'),
            'fltno': col('flight_number'),
            'dep_apt': col('departure_airport'),
            'arr_apt': col('arrival_airport'),
            'scheduled_departure': col('scheduled_departure'),

            # on purpose!
            'actual_departure': col('predicted_departure'),
        }
        writer.writerow(flight)
