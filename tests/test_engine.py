from datetime import datetime, timedelta
from io import StringIO

from flights import engine, factories, models, redis, settings
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
    header = 'carrier,flight_number,dep_apt,arr_apt,scheduled_date,' \
             'scheduled_departure\n'
    row1 = '7I,773,CUR,MAO,2016-04-29,2016-04-29 20:50:00\n'
    row2 = 'AA,1361,PBI,PHL,2016-04-29,2016-04-29 15:55:00\n'

    in_file = StringIO(header + row1 + row2)
    out_file = StringIO()

    redis.set('departure_CUR', {'mean': 100, 'min': 10, 'max': 120})

    engine.predict_redis(in_file, out_file)

    out_file.seek(0)

    assert out_file.readline().strip() == header.strip() + ',actual_departure'

    line1 = out_file.readline().strip()
    assert line1.split(',')[:-2] == row1.strip().split(',')[:-1]
    assert (datetime.strptime(line1.split(',')[-1],
                              settings.DATETIME_FORMAT)
            - datetime(2016, 4, 29, 20, 50)).total_seconds() <= 200

    assert out_file.readline().strip() == row2.strip() + ','


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
