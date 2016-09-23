import csv

import dateutil.parser
import logging

from . import models
from .database import db_session


logger = logging.getLogger(__name__)


def parse_csv(csvfile):
    reader = csv.DictReader(csvfile)
    count = 0

    for row in reader:
        flight = models.Flight(
            carrier=row['carrier'],
            flight_number=row['fltno'],
            departure_airport=row['dep_apt'],
            arrival_airport=row['arr_apt'],
            scheduled_departure=
                dateutil.parser.parse(row['scheduled_departure']),
            actual_departure=
                dateutil.parser.parse(row['actual_departure'])
                if row['actual_departure'] else None,
        )
        db_session.add(flight)
        db_session.commit()

        count += 1
        if count % 1000 == 0:
            logger.info('%d flights imported...' % count)
