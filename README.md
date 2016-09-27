[![Build Status](https://travis-ci.org/mgp4/delays.svg?branch=master)](https://travis-ci.org/mgp4/delays)
[![Coverage Status](https://coveralls.io/repos/github/mgp4/delays/badge.svg?branch=master)](https://coveralls.io/github/mgp4/delays?branch=master)


## Installation

Needed: Python 3.5

1. `virtualenv3 virtualenv`
2. Make sure `virtualenv/bin` is in `PATH`.
3. `pip install -r requirements.txt`
4. Create `flights/settings_local.py` if customized settings are needed.


## Upgrading

Call `pip install -r requirements.txt` to install all missing dependencies.

Call `alembic upgrade head` to upgrade the DB schema.
See [the manual](http://alembic.zzzcomputing.com/en/latest/tutorial.html)
for more info/commands.


## Testing

Run `./test.sh`.
Test coverage is located under the `htmlcov` directory then.
