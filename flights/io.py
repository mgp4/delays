import csv
from datetime import datetime
import logging
import random

from . import models, redis, settings
from .database import db_session, db_engine


logger = logging.getLogger(__name__)

BATCH = 1000


def save_db(flights):
    db_engine.execute(models.Flight.__table__.insert(), flights)


def save_redis(flights):
    with redis.cache.pipeline() as pipe:
        for flight in flights:
            pipe.set('flight_%s_%s' % (flight['flight_number'],
                                       flight['scheduled_departure']),
                     redis.dumps(flight))
        pipe.execute()


def import_csv(csvfile, save=save_db, sparse=False):
    """Imports data from CSV file.

    :param csvfile: opened file
    :param save: saving method, `save_db` or `save_redis`
    :param sparse: degree of sparseness, the greater the sparser
    """

    reader = csv.DictReader(csvfile)
    processed = 0
    imported = 0
    flights = []

    for row in reader:
        if processed % BATCH == 0 and processed:
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
                datetime.strptime(row['scheduled_departure'],
                                  settings.DATETIME_FORMAT),
            'actual_departure':
                datetime.strptime(row['actual_departure'],
                                  settings.DATETIME_FORMAT)
                if row['actual_departure'] else None,
        }
        flights.append(flight)

        processed += 1
        imported += 1

        # bulk saving
        if imported % BATCH == 0 and imported:
            save(flights)
            flights = []
    else:
        # save remaining unsaved flights
        save(flights)

    logger.info('%d flights imported.' % imported)


def load_db():
    yield from models.all_flights()


def load_redis():
    yield from redis.all_flights()


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
