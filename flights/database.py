from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import settings


db_engine = create_engine(settings.DB_URL, encoding='utf-8')
db_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=True,
                 bind=db_engine),
)

Base = declarative_base()
Base.query = db_session.query_property()
