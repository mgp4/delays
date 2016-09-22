from datetime import datetime

from io import StringIO

from flights import models, parser


def test_parser():
    csv_file = StringIO(
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
    parser.parse_csv(csv_file)

    assert models.Flight.query.count() == 7
    assert models.Flight.query.filter_by(flight_number=5202) \
        .one().actual_departure == datetime(year=2016, month=4, day=29,
                                            hour=20, minute=1)
