# -*- coding: utf-8 -*-
import os
import json
import datetime

from schematics.types import \
    StringType as BaseStringType, \
    DateType as BaseDateType, \
    DateTimeType as BaseDateTimeType, \
    BooleanType, DecimalType, BaseType, IntType  # flake8: noqa

from schematics.exceptions import ValidationError
from google.cloud import datastore

from .datastore_client import client as datastore_client


class JSONType(BaseType):

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = {}
        super(JSONType, self).__init__(*args, **kwargs)

    def to_native(self, value, *args, **kwargs):
        if isinstance(value, basestring) and value:
            value = json.loads(value)
        return super(JSONType, self).to_native(value, *args, **kwargs)

    def to_primitive(self, value, *args, **kwargs):
        res = super(JSONType, self).to_primitive(value, *args, **kwargs)
        if isinstance(value, dict):
            return unicode(json.dumps(res))
        return res


class BlobType(BaseType):
    "BlobType"
    # Base type is enough for this
    pass


class StringType(BaseStringType):

    def to_primitive(self, *args, **kwargs):
        value = super(StringType, self).to_primitive(*args, **kwargs)
        if value and not isinstance(value, unicode):
            # Google datastore client only respect unicode as string
            value = unicode(value)
        return value


class DateTimeType(BaseDateTimeType):

    def to_primitive(self, value, *args, **kwargs):
        return value


class DateType(BaseDateType):

    def to_native(self, value, *args, **kwargs):
        if isinstance(value, datetime.datetime):
            value = value.date()
        return super(DateType, self).to_native(value, *args, **kwargs)

    def to_primitive(self, value, *args, **kwargs):
        res = super(DateType, self).to_primitive(value, *args, **kwargs)
        # XXX: GCP Datastore only support DateTime, add minimum time
        if isinstance(value, datetime.date):
            return datetime.datetime.combine(
                value, datetime.datetime.min.time())
        return res


class Many2OneType(BaseType):

    def __init__(self, target, *args, **kwargs):
        from .model import Model

        super(Many2OneType, self).__init__(*args, **kwargs)
        if not issubclass(target, Model):
            raise Exception('Target should be subclass of Model type.')
        self.target = target

    def to_native(self, value, *args, **kwargs):
        if value is None:
            return value
        if isinstance(value, datastore.key.Key):
            if value.kind != self.target._get_kind():
                raise Exception(
                    "Expected key of %s kind, found %s instead." % (
                        self.target._get_kind(), value.kind)
                )
            return self.target.get_by_id(value.id_or_name)
        if isinstance(value, self.target):
            return value
        raise Exception("Unexpected value")

    def to_primitive(self, value, *args, **kwargs):
        return value.datastore_key

    def validate_entity(self, value):
        if value and not isinstance(value, self.target):
            raise ValidationError(
                "Value must be an instance of %s" % self.target._get_kind())


class Many2ManyType(BaseType):

    def __init__(self, target, *args, **kwargs):
        from .model import Model
        if 'default' not in kwargs:
            kwargs['default'] = []
        super(Many2ManyType, self).__init__(*args, **kwargs)
        if not issubclass(target, Model):
            raise Exception('Target should be subclass of Model type.')
        self.target = target

    def to_native(self, value, *args, **kwargs):
        if value is None:
            return []
        if type(value) is list:
            items = []
            keys_to_read = []
            for elm in value:
                if isinstance(elm, self.target):
                    items.append(elm)
                    continue
                if isinstance(elm, datastore.key.Key):
                    if elm.kind != self.target._get_kind():
                        raise Exception(
                            "Expected key of %s kind, found %s instead." % (
                                self.target._get_kind(), elm.kind)
                        )
                    keys_to_read.append(elm)
            if keys_to_read:
                items += self.target.from_entities(
                    datastore_client.get_multi(keys_to_read))
            return items
        return value

    def to_primitive(self, value, *args, **kwargs):
        if value is None:
            return []
        items = []
        for elm in value:
            if elm.id:
                items.append(elm.datastore_key)
        return items

    def validate_entity(self, value):
        for elm in value:
            if elm and not isinstance(elm, self.target):
                raise ValidationError(
                    "Value must be an instance of %s" % self.target._get_kind())
