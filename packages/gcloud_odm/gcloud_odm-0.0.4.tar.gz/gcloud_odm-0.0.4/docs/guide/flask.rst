.. highlight:: python


==================
Flask Support
==================

gcloud odm works with Flask out of the box.


Installing
==========

Install with pip:

.. code-block:: bash

    pip install gcloud_odm[flask]

A minimal application
=====================

For the common case of having one Flask application all you have to do
is to create your Flask application, load the configuration of choice
and then create the GCloudODM object by passing it the application.

.. code-block:: python

    from flask import Flask
    from gcloud_odm.contrib.flask import GCloudODM

    app = Flask(__name__)
    gcloud_odm = GCloudODM(app)


If you are using an application factory pattern::

.. code-block:: python

    gcloud_odm = GCloudODM()

    # and when application is available
    gcloud_odm.init_app(app)


Using the datastore client
==========================

A local proxy to the client is always available
from `gcloud_odm.client`


.. code-block:: python

    from gcloud_odm import client


Configuration
=============

The following configuration values exist for Flask extension.
The app loads these values from your main Flask config which
can be populated in various ways. Note that some of those cannot
be modified after the engine was created so make sure to configure
as early as possible and to not modify them at runtime.

Configuration Keys
------------------

GOOGLE_APPLICATION_CREDENTIALS
```````````````````````````````

Path to the Google Application Credentials JSON file

`/path/to/credentials.json`

GOOGLE_APPLICATION_CREDENTIALS_INFO
```````````````````````````````````

JSON dump of the credentials

GCLOUD_PROJECT
``````````````

(optional)

If the project name is not explicitly configured, it is
picked up from the gcloud config in the environment by
the google cloud api.


GCLOUD_ODM_NAMESPACE
````````````````````

(optional)
