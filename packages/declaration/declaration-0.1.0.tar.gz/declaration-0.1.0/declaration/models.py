import six

from declaration.fields import DeclarativeField


class DeclarativeMeta(type):
    """Metaclass definition that handles creating a hidden property to store a
    dict of the fields"""

    def __new__(cls, name, bases, attrs):
        parent_new = super(DeclarativeMeta, cls).__new__

        filtered_attrs = {}
        fields = {}
        # Loop through all the requested attributes, but filter out the
        # DeclarativeFields so that we can store them separately. Removing them
        # from the generator.attrs allows __getattr__ to work in the
        # DeclarativeBase, since it requires the attribute to actually be
        # missing to run.
        for name, attr in attrs.items():
            if isinstance(attr, DeclarativeField):
                fields[name] = attr
            else:
                filtered_attrs[name] = attr

        generator = parent_new(cls, name, bases, filtered_attrs)
        generator._fields = fields

        return generator


@six.add_metaclass(DeclarativeMeta)
class DeclarativeBase(dict):

    def __iter__(self):
        # Only iterate through the declarative fields, since we inherit dict
        for key, field in six.iteritems(self._fields):
            yield key

    def __setattr__(self, key, value):
        # Only set an attribute if it's part of the declarative fields
        if key in self._fields:
            field = self._fields[key]
            # The field value will store the parsed value. We have to store
            # this separately, which unfortunately causes duplication of memory
            # effort, but we need the raw value stored for attribute access.
            field.value = field.parse(value)
            self[key] = field.encode(field.value)

    def __getattr__(self, key):
        # Return the value that we stored on the field.value property during
        # __setattr__ for attribute access
        if key in self._fields:
            return self._fields[key].value

        return None

    def __getitem__(self, key, encode=True):
        # Return the encoded value that we stored during __setattr__ for
        # dict-like access (i.e. for JSON encoding)
        if key in self._fields:
            value = super(DeclarativeBase, self).__getitem__(key)
            return value

        return None
