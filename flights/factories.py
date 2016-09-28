import random
import string

import factory
from factory import lazy_attribute
from factory.alchemy import SQLAlchemyModelFactory
from faker import Factory

from . import models, io
from .database import db_session


faker = Factory.create()

lazy = lambda call: lazy_attribute(lambda obj: call())
lazy_string = lambda length: lazy(lambda: ''.join(
    [random.choice(string.ascii_uppercase) for _ in range(length)]
))
lazy_carrier = lazy_string(2)
lazy_airport = lazy_string(3)
lazy_date_time = lazy(lambda:
    faker.date_time_between(start_date='-30d', end_date='+30d')
)
#lazy_flight_number = lazy(lambda: ''.join(
#    [random.choice(string.ascii_uppercase) for _ in range(2)] +
#    [random.choice(string.digits) for _ in range(3)]
#))
lazy_flight_number = lazy(lambda: random.randint(100, 10000))


class Flight(SQLAlchemyModelFactory):
    class Meta:
        model = models.Flight
        sqlalchemy_session = db_session

    carrier = lazy_carrier
    flight_number = lazy_flight_number
    departure_airport = lazy_airport
    arrival_airport = lazy_airport
    scheduled_departure = lazy_date_time
    actual_departure = lazy_date_time  # TODO = scheduled +/- few hours


def json_flight(**kwargs):
    return factory.build(dict, FACTORY_CLASS=Flight, **kwargs)


def redis_flight(**kwargs):
    flight = json_flight(**kwargs)
    io.save_redis(flight)
    return flight
