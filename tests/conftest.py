import pytest

from flights import settings
settings.DB_URL = 'sqlite:///:memory:'
settings.REDIS_CONFIG = settings.REDIS_TEST_CONFIG

from flights import models, redis


@pytest.fixture(scope='session', autouse=True)
def db_prepare():
    models.create_db()


@pytest.yield_fixture(scope='function', autouse=True)
def db_clean():
    redis.cache.flushdb()
    models.Flight.query.delete()
    yield
