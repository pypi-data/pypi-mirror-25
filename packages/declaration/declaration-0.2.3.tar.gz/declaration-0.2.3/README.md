# Declaration
Declarative models and fields for Python objects, similar to how many Python ORMs work. Includes automatic support for JSON encoding with no custom encoder required.

[![Build Status](https://travis-ci.org/boomletsgo/declaration.svg?branch=master)](https://travis-ci.org/boomletsgo/declaration)
[![PyPI](https://img.shields.io/pypi/v/declaration.svg)](https://pypi.python.org/pypi/declaration/)
[![Python Versions](https://img.shields.io/pypi/pyversions/declaration.svg)](https://pypi.python.org/pypi/declaration/)
[![Coverage Status](https://coveralls.io/repos/boomletsgo/declaration/badge.svg?branch=master)](https://coveralls.io/r/boomletsgo/declaration?branch=master)




## Installation

`$ pip install declaration`

## Usage

Inside your application file:

```
import datetime
import json

from declaration import fields, models

class Person(models.DeclarativeBase):
	first_name = fields.StringField()
	last_name = fields.StringField()
	join_date = fields.DateTimeField()
	# See fields.py for a complete list of fields

me = Person()
me.first_name = "Joe"
me.last_name = "Somebody"
me.join_date = datetime.datetime.now()

json.dumps(me)
```

## Field Types

* DeclarativeField - Base field type. Make your own types by inheriting from this.
* GenericField - Passes values through with no parsing or encoding.
* StringField - Sends and receives strings. Coerces to string if necessary.
* UUIDField - Sends and receives UUIDs and UUID v4-formatted strings.
* DateTimeField - Sends and receives datetime objects. Parses using python-dateutil.
* DateField - Sends and receives date objects. Parses using python-dateutil and can accept a datetime.
* TimeField - Sends and receives time objects. Can accept a datetime.
* JSONField - Sends and receives JSON objects. Must be able to be loaded and encoded through json.loads and json.dumps.

The normal use case for declarative models and fields is for ORMs and business objects. You could use it for APIs and SDKs, or to pass data between systems via JSON. All JSON encoding is done automatically based on the field type you use.

If you need a new field or have a suggestion, please create an issue or PR!
