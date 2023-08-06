.. highlight:: python


==================
Defining entities
==================

An Entity is roughly equivalent to a **row** in a relational database.
When working with relational databases, rows are stored in tables,
which have a strict **schema** that the rows follow. Datastore stores
entities in one giant pool and the different types of entities are
identified by **Kind**.

Objects in Cloud Datastore are known as entities, and each entity is of a
particular kind. By building a class inheriting from Model, you can create
an object that enforces structure for a *Kind* of Entity.

The principal difference however, is that no schema is enforced by
the datastore.

Defining an entity's schema
===========================

gcloud odm allows you to define the schema for entities as this helps
to reduce coding errors and gives structure to your code.

To define a schema for an entity, create a class that inherits from
:class:`~gcloud_odm.Model`. Fields are specified by adding fields
instances as class attributes to the Entity class::

    import gcloud_odm
    from datetime import datetime

    class Greeting(gcloud_odm.Model):
        """
        Models an individual Guestbook
        entry with content and date.
        """
        content = gcloud_odm.StringType(max_length=200)
        date = gcloud_odm.DateTimeType(default=datetime.utcnow)

Fields
======

Fields in gcloud odm are powered by schematics and some
field types have datastore specific changes.

* :class:`~gcloud_odm.types.StringType`
* :class:`~gcloud_odm.types.JSONType`
* :class:`~gcloud_odm.types.DateTimeType`
* :class:`~gcloud_odm.types.DateType`
* :class:`~gcloud_odm.types.BlobType`
* :class:`~gcloud_odm.types.IntType`
* :class:`~gcloud_odm.types.BooleanType`
* :class:`~gcloud_odm.types.Many2OneType`
* :class:`~gcloud_odm.types.Many2ManyType`


Field arguments
---------------
Each field type can be customized by keyword arguments.  The following keyword
arguments can be set on all fields:

:attr:`required`:
    Invalidate field when value is None or is not supplied. Default:
    False.
:attr:`default`:
    When no data is provided default to this value. May be a callable.
    Default: None.
:attr:`serialized_name`:
    The name of this field defaults to the class attribute used in the
    model. However if the field has another name in foreign data set this
    argument. Serialized data will use this value for the key name too.
:attr:`deserialize_from`:
    A name or list of named fields for which foreign data sets are
    searched to provide a value for the given field.  This only effects
    inbound data.
:attr:`choices`:
    A list of valid choices. This is the last step of the validator
    chain.
:attr:`validators`:
    A list of callables. Each callable receives the value after it has been
    converted into a rich python type. Default: []
:attr:`serialize_when_none`:
    Dictates if the field should appear in the serialized data even if the
    value is None. Default: True
:attr:`messages`:
    Override the error messages with a dict. You can also do this by
    subclassing the Type and defining a `MESSAGES` dict attribute on the
    class. A metaclass will merge all the `MESSAGES` and override the
    resulting dict with instance level `messages` and assign to
    `self.messages`.
:attr:`metadata`:
    Dictionary for storing custom metadata associated with the field.
    To encourage compatibility with external tools, we suggest these keys
    for common metadata:
    - *label* : Brief human-readable label
    - *description* : Explanation of the purpose of the field. Used for
      help, tooltips, documentation, etc.

Validation
----------

Fields also may have validation constraints available
(such as :attr:`max_length` in the example above).
