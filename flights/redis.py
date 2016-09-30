from datetime import datetime
import json

from redis import StrictRedis

from . import settings


cache = StrictRedis(**settings.REDIS_CONFIG)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime(settings.DATETIME_FORMAT)
        return super().default(o)


def datetime_hook(result):
    for key, value in result.items():
        if key.endswith('departure') and value not in ['', None]:
            result[key] = datetime.strptime(value, settings.DATETIME_FORMAT)
    return result


def get(key):
    value = cache.get(key)
    return json.loads(value.decode(), object_hook=datetime_hook) if value \
           else None


def dumps(value):
    return json.dumps(value, cls=JSONEncoder)


def set(key, value):
    return cache.set(key, dumps(value))


def _count(match):
    return len(list(cache.scan_iter(match)))


def all_flights():
    for key in cache.scan_iter('flight_*'):
        yield get(key)
