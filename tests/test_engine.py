from datetime import datetime, timedelta

from flights import engine, factories, models, redis
from flights.database import db_session


N = 40


def test_predict_db():
    [factories.Flight() for _ in range(N)]
    db_session.commit()

    engine.predict_db()

    assert models.Flight.query.count() == N
    assert isinstance(models.Flight.query.first().predicted_departure,
                      datetime)


def test_predict_redis():
    [factories.redis_flight() for _ in range(N)]

    engine.predict_redis()

    assert len(list(redis.cache.scan_iter('flight_*'))) == N
    assert isinstance(
        redis.get(next(redis.cache.scan_iter('flight_*')))
            ['predicted_departure'],
        datetime
    )


def test_compute_diff_db():
    factories.Flight(actual_departure=datetime(year=2016, month=4, day=29,
                                               hour=20, minute=1),
                     predicted_departure=datetime(year=2016, month=4, day=29,
                                                  hour=22, minute=6))
    factories.Flight(actual_departure=datetime(year=2016, month=4, day=29,
                                               hour=20, minute=1),
                     predicted_departure=datetime(year=2016, month=4, day=29,
                                                  hour=18, minute=2))
    db_session.commit()

    diff = engine.compute_diff_db()

    assert diff['sum'] == timedelta(hours=4, minutes=4)


def test_compute_diff_redis():
    factories.redis_flight(
        actual_departure=datetime(year=2016, month=4, day=29,
                                  hour=20, minute=1),
        predicted_departure=datetime(year=2016, month=4, day=29,
                                     hour=22, minute=6)
    )
    factories.redis_flight(
        actual_departure=datetime(year=2016, month=4, day=29,
                                  hour=20, minute=1),
        predicted_departure=datetime(year=2016, month=4, day=29,
                                     hour=18, minute=2)
    )

    diff = engine.compute_diff_redis()

    assert diff['sum'] == timedelta(hours=4, minutes=4)
