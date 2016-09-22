import csv

import dateutil.parser

from . import models
from .database import db_session


def parse_csv(csvfile):
    reader = csv.DictReader(csvfile)
    for row in reader:
        flight = models.Flight(
            carrier=row['carrier'],
            flight_number=row['fltno'],
            departure_airport=row['dep_apt'],
            arrival_airport=row['arr_apt'],
            scheduled_departure=dateutil.parser.parse(
                row['scheduled_departure']
            ),
            actual_departure=dateutil.parser.parse(row['actual_departure']),
        )
        db_session.add(flight)
        db_session.commit()
