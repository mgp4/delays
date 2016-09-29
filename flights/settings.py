import logging.config


DB_URL = 'sqlite:///:memory:'

REDIS_CONFIG = {}
REDIS_TEST_CONFIG = {}


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


LOGGING = lambda: {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

try:
    from .settings_local import *
except ImportError:
    pass


LOGGING = LOGGING()
logging.config.dictConfig(LOGGING)
