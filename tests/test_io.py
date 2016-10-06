from datetime import datetime

from io import StringIO

from flights import io, models, factories, redis
from flights.database import db_session


N = 40

csv_file = lambda: StringIO(
    'carrier,fltno,dep_apt,arr_apt,sched_departure_date,'
    'scheduled_departure,actual_departure\n'
    '7I,773,CUR,MAO,2016-04-29,2016-04-29 20:50:00,2016-04-30 19:15:00\n'
    'AA,1361,PBI,PHL,2016-04-29,2016-04-29 15:55:00,2016-04-30 08:21:00\n'
    'AA,137,DFW,HKG,2016-04-29,2016-04-29 07:50:00,2016-04-29 12:28:00\n'
    'AA,4173,LGA,STL,2016-04-29,2016-04-29 17:10:00,2016-04-29 16:58:00\n'
    'AA,5202,GNV,CLT,2016-04-29,2016-04-29 17:50:00,2016-04-29 20:01:00\n'
    'AA,5633,PHX,TUS,2016-04-29,2016-04-29 17:20:00,2016-04-29 21:31:00\n'
    'AA,6159,MIA,LHR,2016-04-29,2016-04-29 17:05:00,2016-04-30 20:05:00'
)


def test_import_db():
    io.import_csv(csv_file(), save=io.save_db)

    assert models.Flight.query.count() == 7
    assert models.Flight.query.filter_by(flight_number=5202) \
        .one().actual_departure == datetime(year=2016, month=4, day=29,
                                            hour=20, minute=1)


def test_import_redis():
    io.import_csv(csv_file(), save=io.save_redis)

    assert redis.get('flight_5202_2016-04-29 17:50:00') \
        ['actual_departure'] == datetime(year=2016, month=4, day=29,
                                         hour=20, minute=1)


def test_import_airports():
    csv_file = StringIO("""\
507,"Heathrow","London","United Kingdom","LHR","EGLL",51.4775,-0.461389,83,0,"E","Europe/London"
26,"Kugaaruk","Pelly Bay","Canada","YBB","CYBB",68.534444,-89.808056,56,-7,"A","America/Edmonton"
3127,"Pokhara","Pokhara","Nepal","PKR","VNPK",28.200881,83.982056,2712,5.75,"N","Asia/Katmandu"\
    """)
    io.import_airports(csv_file)

    assert models.Airport.query.count() == 3
    airport = models.Airport.query.filter_by(code='PKR').one()
    assert airport.name == 'Pokhara'
    assert abs(airport.latitude - 28.2) < 0.001


def test_export_db():
    [factories.Flight(predicted_departure=factories.fake_date_time())
            for _ in range(N)]
    db_session.commit()

    csvfile = StringIO()
    io.export_csv(csvfile, load=io.load_db)

    models.Flight.query.delete()
    csvfile.seek(0)
    io.import_csv(csvfile, save=io.save_db)
    assert models.Flight.query.count() == N


def test_export_redis():
    [factories.redis_flight(predicted_departure=factories.fake_date_time())
            for _ in range(N)]

    csvfile = StringIO()
    io.export_csv(csvfile, load=io.load_redis)

    redis.cache.flushdb()
    csvfile.seek(0)
    io.import_csv(csvfile, save=io.save_redis)
    assert redis._count('flight_*') == N
