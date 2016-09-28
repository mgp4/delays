import csv

import dateutil.parser
import logging

from . import models, redis
from .database import db_session


logger = logging.getLogger(__name__)


def save_db(flight):
    flight.update({
        'scheduled_departure':
            dateutil.parser.parse(flight['scheduled_departure']),
        'actual_departure':
            dateutil.parser.parse(flight['actual_departure'])
            if flight['actual_departure'] else None,
    })
    db_session.add(models.Flight(**flight))
    db_session.commit()


def save_redis(flight):
    redis.set('flight_%s_%s' % (flight['flight_number'],
                                flight['scheduled_departure']),
              flight)


def import_csv(csvfile, save=save_db):
    reader = csv.DictReader(csvfile)
    count = 0

    for row in reader:
        flight = {
            'carrier': row['carrier'],
            'flight_number': row['fltno'],
            'departure_airport': row['dep_apt'],
            'arrival_airport': row['arr_apt'],
            'scheduled_departure': row['scheduled_departure'],
            'actual_departure': row['actual_departure'],
        }
        save(flight)

        count += 1
        if count % 1000 == 0:
            logger.info('%d flights imported...' % count)