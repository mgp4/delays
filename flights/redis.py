from datetime import datetime
import json

from redis import StrictRedis

from . import settings


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

cache = StrictRedis(**settings.REDIS_CONFIG)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime(DATETIME_FORMAT)
        return super().default(o)


def datetime_hook(result):
    for key, value in result.items():
        if key.endswith('departure') and value not in ['', None]:
            result[key] = datetime.strptime(value, DATETIME_FORMAT)
    return result


def get(key):
    value = cache.get(key)
    return json.loads(value.decode(), object_hook=datetime_hook) if value \
           else None


def set(key, value):
    return cache.set(key, json.dumps(value, cls=JSONEncoder))


def _count(match):
    return len(list(cache.scan_iter(match)))
