import pytest

from flights import settings
settings.DB_URL = 'sqlite:///:memory:'

from flights import models


@pytest.fixture(scope='session', autouse=True)
def db_prepare():
    models.create_db()


@pytest.yield_fixture(scope='function', autouse=True)
def db_clean():
    yield
    models.Flight.query.delete()
