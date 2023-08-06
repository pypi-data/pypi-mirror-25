# -*- coding: utf-8 -*-
"""
    model

    :license: see LICENSE for details.
"""
from datetime import datetime

from schematics.models import Model as BaseModel
from google.cloud.datastore.entity import Entity

from .types import DateTimeType, IntType
from .datastore_client import client as datastore_client


class Model(BaseModel):
    _index_fields = []
    _entity_kind = None
    _entity = None

    id = IntType()
    created_at = DateTimeType(default=datetime.utcnow)
    updated_at = DateTimeType()

    def __repr__(self):
        repr = super(Model, self).__repr__()
        return "%s (%s)" % (repr, self.id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if other._get_kind() != self._get_kind():
            # has to be of the same model
            return False
        if self.id and (other.id != self.id):
            # If the record has an ID the other one should
            # have the same.
            return False
        if not self.id:
            # Unsaved records are same only if _fields data
            # of both are the same.
            for k in self._fields:
                if self._data[k] != other._data[k]:
                    return False
        return True

    @property
    def _non_indexed(self):
        return list(set(self._fields.keys()) - set(self._index_fields))

    @property
    def datastore_key(self):
        """Returns datastore key for this entity
        """
        if self._entity:
            return self._entity.key

    @classmethod
    def get_by_id(cls, id):
        """Returns
        """
        records = cls.get_by_ids([id], ignore_missing=True)
        if records:
            return records[0]

    @classmethod
    def get_by_ids(cls, ids, ignore_missing=False):
        """Retrieve entities, along with their attributes.

        :type ids: list of ids(string/number)
        :param ids: The ids to be retrieved from the datastore.

        :type ignore_missing: Boolean
        :param ignore_missing: (Optional) If True not found keys will be
                               ignored, else ValueError will be raised.
        :rtype: list of :class:`gcloud_odm.model.Model`
        :returns: The requested objects.
        :raises: :class:`ValueError` if one or more ``ids`` are invalid.
        """
        keys = map(
            lambda id: datastore_client.key(cls._get_kind(), id), ids)
        missing = []
        entities = datastore_client.get_multi(keys, missing=missing)
        if not ignore_missing and missing:
            raise ValueError("Some keys are missing")
        return cls.from_entities(entities)

    @classmethod
    def from_entity(cls, entity):
        assert entity.key.kind == cls._get_kind(), (
            "Expected entity of kind '%s', found '%s' instead." % (
                cls._get_kind(), entity.key.kind
            )
        )

        # Build raw data
        raw_data = {}
        for k, v in entity.items():
            if k in cls._fields.keys():
                raw_data[k] = v
        raw_data['id'] = entity.key.id_or_name

        instance = cls(raw_data=raw_data)
        instance._entity = entity
        return instance

    @classmethod
    def from_entities(cls, entities):
        return map(cls.from_entity, entities)

    @classmethod
    def query(cls):
        return datastore_client.query(kind=cls._get_kind())

    @classmethod
    def _get_kind(cls):
        return cls._entity_kind or cls.__name__

    def _get_entity(self):
        if self._entity is None:
            if self.id:
                key = datastore_client.key(self._get_kind(), self.id)
            else:
                key = datastore_client.key(self._get_kind())
            self._entity = Entity(key, exclude_from_indexes=self._non_indexed)
        return self._entity

    def save(self):
        """Save the entity
        """
        self.updated_at = datetime.utcnow()
        self.validate()
        entity = self._get_entity()
        data = self.to_primitive()
        data.pop('id', None)
        entity.update(data)
        datastore_client.put(entity)
        # Update id
        self.id = entity.key.id_or_name

    def delete(self):
        """Delete the entity.
        """
        datastore_client.delete(self.datastore_key)
