import datetime


class DeclarativeField(object):

    def __init__(self):
        self.value = None

    def parse(self, value):
        raise NotImplementedError

    def encode(self, value):
        raise NotImplementedError


class GenericField(DeclarativeField):

    def parse(self, value):
        return value

    def encode(self, value):
        return value


class StringField(GenericField):

    def parse(self, value):
        return str(value)

    def encode(self, value):
        return str(value)


class DateTimeField(GenericField):

    def encode(self, value):
        return value.isoformat()


class DateField(DateTimeField):

    def parse(self, value):
        if isinstance(value, datetime.datetime):
            value = value.date()

        return value


class TimeField(DateTimeField):

    def parse(self, value):
        if isinstance(value, datetime.datetime):
            value = value.time()

        return value
