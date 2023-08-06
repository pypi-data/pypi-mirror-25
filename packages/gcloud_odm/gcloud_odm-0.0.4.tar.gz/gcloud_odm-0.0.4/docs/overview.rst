.. highlight:: python

Overview
========

This library allows Python apps to connect to Google Cloud Datastore.
The library builds on top of Schematics to provide a SQL table like
structure.

Getting Started
---------------


Using Models for storing data
-----------------------------

Cloud Datastore is schemaless, which means that no schema is enforced by the
database. While this makes life a lot easier in many regards, defining schemas for
entities can help to reduce errors from missing fields and enforce type safety.

Besides, models give you a convenient way to access entities like the way you
would with Django's ORM or SQL Alchemy.


Defining an Entity
```````````````````

Objects in Cloud Datastore are known as entities, and each entity is of a
particular kind. By building a class inheriting from Model, you can create
an object that enforces structure for a *Kind* of Entity.


.. code-block:: python


    import gcloud_odm
    from datetime import datetime


    class Greeting(gcloud_odm.Model):
        """
        Models an individual Guestbook
        entry with content and date.
        """
        content = gcloud_odm.StringType(max_length=200)
        date = gcloud_odm.DateTimeType(default=datetime.utcnow)


Adding data
```````````

Now that we’ve defined how our entity will be structured,
let’s start adding some entities.

Firstly, we’ll need to create a Greeting object::


.. code-block:: python

    greeting = Greeting({'content': 'Hello World'})
    greeting.save()

Alternatively, you can also define entity properties using
the attribute syntax


.. code-block:: python

    greeting = Greeting()
    greeting.content = 'Hello World'
    greeting.save()


For ndb users, `put()` works as an alternative to `save()`.

.. code-block:: python

    greeting = Greeting({'content': 'Hello World'})
    greeting.put()


Example of creating a new entry in a Flask request


.. code-block:: python


    @app.route('/greetings/new', methods=['POST'])
    def new_greeting():
        "Create a new greeting on post"
        greeting = Greeting({
            'content': request.form['content']
        })
        greeting.save()


To create and store a new greeting, the application creates a
new `Greeting` object and calls its `save()` method. On calling
`save()` the entity is `put` to the datastore.


Accessing data
``````````````

Each Model class has an `objects` attribute, which is used to
access the entities in the associated datastore.

.. code-block:: python

    for greeting in Greeting.objects:
        print(greeting.comment)


Running a raw query
```````````````````

You can also use the `query` object from datastore python client
from the query attribute of Model.

.. code-block:: python

    query = Greeting.query
    query.order = ['date']
    return list(query.fetch())


However, remember that the objects returned when using the query
object are entities from the underlying gcloud python API and
**not** instances of the model. You can convert the entities
into model instances using

.. code-block:: python

    greeting_1 = Greeting.from_entity(entity)

or for a list of entities using

.. code-block:: python

    greetings = Greeting.from_entities([entity1, entity2])



Deleting entities
`````````````````

To delete an entity, call the `delete()` method. Note that this will
only work if the entity exists in the datastore and has a valid id.

.. code-block:: python

    greeting = Greeting.objects.get(id=1)
    greeting.delete()
