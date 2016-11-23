# Flight delays predictor

[![Build Status](https://travis-ci.org/mgp4/delays.svg?branch=master)](https://travis-ci.org/mgp4/delays)
[![Coverage Status](https://coveralls.io/repos/github/mgp4/delays/badge.svg?branch=master)](https://coveralls.io/github/mgp4/delays?branch=master)
[![Documentation Status](https://readthedocs.org/projects/delays/badge/?version=latest)](http://delays.readthedocs.io/en/latest/?badge=latest)

This is our solution to [a competition](https://datachallenge.cz/)
organized by [Kiwi.com](https://www.kiwi.com).

The official task assignment is backed up in [task.html](task.html)
and the results are stored in [results.html](results.html).

## Requirements

- Python >= 3.4
- Database: PostgreSQL preferred (big queries can be batched)
- Redis


## Installation

1. `virtualenv3 [--system-site-packages] virtualenv`
2. Make sure `virtualenv/bin` is in `PATH`.
3. `pip install -r requirements.txt`


## Settings

Create `flights/settings_local.py` if customized settings are needed, e.g.:

```py
DB_URL = 'postgresql://user:password@localhost/db_name'
REDIS_CONFIG = {'db': 4}
REDIS_TEST_CONFIG = {'db': 11}
```

See more info for:

- [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)
- [Redis](https://redis-py.readthedocs.io/en/latest/#redis.StrictRedis)

Call `alembic upgrade head` to create the DB schema.


## Usage

`app.py` is the central executable script.
See `./app.py --help` for options.


## Upgrading

Call `pip install -r requirements.txt` to install all missing dependencies.

Call `alembic upgrade head` to upgrade the DB schema.
See [the manual](http://alembic.zzzcomputing.com/en/latest/tutorial.html)
for more info/commands.


## Notebooks

Call `cd notebooks; PYTHONPATH=.. jupyter notebook [--no-browser]`.
The Jupyter server is listening
at [http://localhost:8888/](http://localhost:8888/) then.


## Testing

Run `./test.sh`.
Test coverage is located under the `htmlcov` directory then.


## Documentation

Run `make clean html` under the `doc` directory.
Generated documentation is located under the `doc/_build/html` directory then.
