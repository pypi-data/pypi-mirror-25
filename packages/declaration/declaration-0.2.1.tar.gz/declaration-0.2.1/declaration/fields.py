import datetime
import json
import uuid

from dateutil import parser
import six


class DeclarativeField(object):

    def parse(self, value):
        raise NotImplementedError

    def encode(self, value):
        raise NotImplementedError


class GenericField(DeclarativeField):

    def parse(self, value):
        return value

    def encode(self, value):
        return value


class UUIDField(GenericField):

    def parse(self, value):
        if not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value, version=4)
            except ValueError:
                pass

        return value

    def encode(self, value):
        if isinstance(value, uuid.UUID):
            return str(value)

        return value


class StringField(GenericField):

    def parse(self, value):
        return str(value)

    def encode(self, value):
        return str(value)


class JSONField(GenericField):

    def parse(self, value):
        if value:
            return json.loads(value)

        return value

    def encode(self, value):
        if value:
            return json.dumps(value)

        return value


class DateTimeField(GenericField):

    def parse(self, value):
        if not isinstance(value, datetime.datetime):
            value = parser.parse(value)

        return value

    def encode(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")


class DateField(DateTimeField):

    def parse(self, value):
        if isinstance(value, six.string_types):
            value = parser.parse(value)

        if isinstance(value, datetime.datetime):
            value = value.date()

        return value


class TimeField(DateTimeField):

    def parse(self, value):
        if isinstance(value, datetime.datetime):
            value = value.time()

        return value
