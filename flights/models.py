import logging

from sqlalchemy import (
    Column, Integer, DateTime, String,
    Table, ForeignKey,
)
from sqlalchemy.orm import relationship

from .database import Base, db_engine


logger = logging.getLogger(__name__)


class Flight(Base):
    __tablename__ = 'flight'

    carrier = Column(String(2), nullable=False)
    flight_number = Column(Integer, nullable=False, primary_key=True)
    departure_airport = Column(String(3), nullable=False)
    arrival_airport = Column(String(3), nullable=False)
    scheduled_departure = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)

    def __repr__(self):
        return '<Flight %s>' % self.flight_number

    def __str__(self):
        return ('%(flight_number)s: '
                '%(departure_airport)s -> %(arrival_airport)s '
                '@ %(actual_departure)s (sched. %(scheduled_departure)s)'
                % self.__dict__)


def create_db():
    """Creates the DB schema."""

    logger.info('Creating DB schema...')
    Base.metadata.create_all(db_engine)
