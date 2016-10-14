import csv
from datetime import datetime, timedelta
import logging

import numpy as np

from . import models, redis, settings
from .database import db_session

logger = logging.getLogger(__name__)


def predict_db():
    for flight in models.all_flights():
        flight.predicted_departure = flight.scheduled_departure
        db_session.flush()
    db_session.commit()


def predict_redis(in_file, out_file):
    reader = csv.DictReader(in_file)

    fieldnames = ['carrier', 'flight_number', 'dep_apt', 'arr_apt',
                  'scheduled_date', 'scheduled_departure', 'actual_departure']
    writer = csv.DictWriter(out_file, fieldnames)
    writer.writeheader()

    for row in reader:
        try:
            stat = redis.get('departure_%s' % row['dep_apt'])
            loc = stat['mean']
            scale = min(abs(stat['max'] - stat['mean']),
                        abs(stat['mean'] - stat['min'])) / 100.0
            row['actual_departure'] = (
                datetime.strptime(row['scheduled_departure'],
                                  settings.DATETIME_FORMAT)
                + timedelta(seconds=np.random.normal(loc, scale))
            ).strftime(settings.DATETIME_FORMAT)
        except Exception as e:
            logger.warning(e)
            row['actual_departure'] = ''
        writer.writerow(row)


def compute_diff_db():
    sum_ = timedelta()
    count = 0
    for flight in models.all_flights():
        if flight.actual_departure and flight.predicted_departure:
            sum_ += abs(flight.predicted_departure - flight.actual_departure)
            count += 1
    return {'sum': sum_, 'count': count, 'avg': sum_ / count}


def compute_diff_redis():
    sum_ = timedelta()
    count = 0
    for flight_key in redis.cache.scan_iter('flight_*'):
        flight = redis.get(flight_key)
        if flight['actual_departure'] and 'predicted_departure' in flight \
                and flight['predicted_departure']:
            sum_ += abs(flight['predicted_departure']
                        - flight['actual_departure'])
            count += 1
    return {'sum': sum_, 'count': count, 'avg': sum_ / count}
