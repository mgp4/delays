import logging

from sqlalchemy import (
    Column, Integer, SmallInteger, Numeric, Float, DateTime, String,
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
    departure_airport = Column(String(3), ForeignKey("airport.code"), index=True, nullable=False)
    arrival_airport = Column(String(3), ForeignKey("airport.code"), index=True, nullable=False)
    scheduled_departure = Column(DateTime, index=True, nullable=True)
    actual_departure = Column(DateTime, index=True, nullable=True)
    predicted_departure = Column(DateTime, nullable=True)
    delay_mins = Column(Integer, index=True, nullable=True)

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


    src_airport = relationship("Airport", foreign_keys=[departure_airport])
    dst_airport = relationship("Airport", foreign_keys=[arrival_airport])


class Airport(Base):
    __tablename__ = 'airport'

    id = Column(Integer, primary_key=True)
    name = Column(String(70))
    city = Column(String(50))
    country = Column(String(40))
    code = Column(String(3), index=True, unique=True)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(SmallInteger)
    tz_offset = Column(Numeric)
    dst = Column(String(1))
    tz_name = Column(String(30))

    def __repr__(self):
        return '<Airport %s>' % self.code


def all_flights():
    return Flight.query.yield_per(YIELD_PER)


def create_db():
    """Creates the DB schema."""

    logger.info('Creating DB schema...')
    Base.metadata.create_all(db_engine)
