# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from mongoengine import Document
from flask_restive.utils import classproperty, plural, decapitalize


def get_collection_name(class_):
    return plural(decapitalize(class_.__name__))


class Model(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True,
        'collection': get_collection_name
    }

    def __init__(self, **kwargs):
        super(Model, self).__init__()
        self.set_attrs(**kwargs)

    def set_attrs(self, **attrs):
        for attr_name, attr_value in attrs.items():
            # pylint: disable=unsupported-membership-test
            if attr_name in self.fields:
                setattr(self, attr_name, attr_value)

    def to_dict(self):
        result = {}
        for attr_name in self.fields:  # pylint: disable=not-an-iterable
            attr_value = getattr(self, attr_name)
            if attr_value is not None:
                result[attr_name] = attr_value
        return result

    @classmethod
    def get_collection(cls):
        return cls._get_collection()

    @classproperty
    def fields(cls):
        # pylint: disable=no-self-argument
        fields = OrderedDict([
            (field_name, field)
            for field_name, field in cls._fields.items()
            if not field_name.startswith('_')
        ])
        return fields

    @classproperty
    def primary_key_fields(cls):
        # pylint: disable=no-self-argument
        fields = OrderedDict([
            (field_name, field)
            for field_name, field in cls._fields.items()
            if field.primary_key
        ])
        return fields
