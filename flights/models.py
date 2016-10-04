import logging

from sqlalchemy import (
    Column, Integer, DateTime, String,
    Table, Index, ForeignKey,
)
from sqlalchemy.orm import relationship

from .database import Base, db_engine


logger = logging.getLogger(__name__)

YIELD_PER = 100


class Flight(Base):
    __tablename__ = 'flight'

    id = Column(Integer, primary_key=True)
    carrier = Column(String(3), index=True, nullable=False)
    flight_number = Column(String(5), index=True, nullable=False)
    departure_airport = Column(String(3), index=True, nullable=False)
    arrival_airport = Column(String(3), index=True, nullable=False)
    scheduled_departure = Column(DateTime, index=True, nullable=True)
    actual_departure = Column(DateTime, index=True, nullable=True)
    predicted_departure = Column(DateTime, nullable=True)

    __table_args__ = (
        Index('flight_stop', 'carrier', 'flight_number', 'scheduled_departure'),
    )

    def __repr__(self):
        return '<Flight %s>' % self.id

    def __str__(self):
        return ('%(flight_number)s: '
                '%(departure_airport)s -> %(arrival_airport)s '
                '@ %(actual_departure)s (sched. %(scheduled_departure)s)'
                % self.__dict__)


def all_flights():
    return Flight.query.yield_per(YIELD_PER)


def create_db():
    """Creates the DB schema."""

    logger.info('Creating DB schema...')
    Base.metadata.create_all(db_engine)
