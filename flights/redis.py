import json

from redis import StrictRedis

from . import settings


cache = StrictRedis(**settings.REDIS_CONFIG)


def get(key):
    value = cache.get(key)
    return json.loads(value.decode()) if value else None


def set(key, value):
    return cache.set(key, json.dumps(value))
