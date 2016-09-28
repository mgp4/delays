from . import models, redis
from .database import db_session


def predicate_db():
    for flight in models.Flight.query.all():
        flight.predicted_departure = flight.scheduled_departure
        db_session.add(flight)
        db_session.commit()


def predicate_redis():
    for flight_key in list(redis.cache.scan_iter('flight_*')):
        flight = redis.get(flight_key)
        flight['predicted_departure'] = flight['scheduled_departure']
        redis.set(flight_key, flight)
