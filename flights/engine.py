from datetime import timedelta

from . import models, redis
from .database import db_session


def predict_db():
    for flight in models.all_flights():
        flight.predicted_departure = flight.scheduled_departure
        db_session.flush()
    db_session.commit()


def predict_redis():
    for flight_key in list(redis.cache.scan_iter('flight_*')):
        flight = redis.get(flight_key)
        flight['predicted_departure'] = flight['scheduled_departure']
        redis.set(flight_key, flight)


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
