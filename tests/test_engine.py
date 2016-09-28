from datetime import datetime

import dateutil.parser

from flights import engine, factories, models, redis
from flights.database import db_session


N = 40


def test_predicate_db():
    [factories.Flight() for _ in range(N)]
    db_session.commit()

    engine.predicate_db()

    assert models.Flight.query.count() == N
    assert type(models.Flight.query.first().predicted_departure) == datetime


def test_predicate_redis():
    [factories.redis_flight() for _ in range(N)]

    engine.predicate_redis()

    assert len(list(redis.cache.scan_iter('flight_*'))) == N
    assert dateutil.parser.parse(
        redis.get(next(redis.cache.scan_iter('flight_*')))
            ['predicted_departure']
    )
