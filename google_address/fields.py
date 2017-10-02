from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignObject
from google_address.models import Address

try:
    from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
except ImportError:
    from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor as ForwardManyToOneDescriptor

# Python 3 fixes.
import sys
if sys.version > '3':
    long = int
    basestring = (str, bytes)
    unicode = str


class AddressDescriptor(ForwardManyToOneDescriptor):

    def __set__(self, inst, value):
        super(AddressDescriptor, self).__set__(inst, self.to_python(value))

    def to_python(self, value):

        if value is None:
            return None

        # Is it already an address object?
        if isinstance(value, Address):
            return value

        # If we have an integer, assume it is a model primary key. This is mostly for
        # Django being a cunt.
        elif isinstance(value, (int, long)):
            try:
                return Address.objects.get(pk=value)
            except Address.DoesNotExist:
                raise ValidationError('Invalid address id.')

        # A string is considered a raw value.
        elif isinstance(value, basestring):
            obj = Address(raw=value)
            obj.save()
            return obj

        # A dictionary of named address components.
        elif isinstance(value, dict):
            return self.from_dict()

        # Not in any of the formats I recognise.
        raise ValidationError('Invalid address value.')

    def from_dict(self):
        raise NotImplementedError()


class AddressField(models.ForeignKey):
    description = 'An address'

    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'google_address.address'
        super(AddressField, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(ForeignObject, self).contribute_to_class(cls, name, virtual_only=virtual_only)
        setattr(cls, self.name, AddressDescriptor(self))