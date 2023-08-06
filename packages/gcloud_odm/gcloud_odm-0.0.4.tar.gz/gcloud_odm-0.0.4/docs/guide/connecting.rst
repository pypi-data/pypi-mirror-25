Authentication
**************

.. _Overview:

Overview
========


If you're running in Compute Engine or App Engine
-------------------------------------------------

Authentication should "just work".


If you're developing locally
----------------------------

the easiest way to authenticate is using the `Google Cloud SDK`_:

.. code-block:: bash

    $ gcloud beta auth application-default login

Note that this command generates credentials for client libraries.
To authenticate the CLI itself, use:

.. code-block:: bash

    $ gcloud auth login

Previously, ``gcloud auth login`` was used for both use cases. If
your ``gcloud`` installation does not support the new command,
please update it:

.. code-block:: bash

    $ gcloud components update

.. _Google Cloud SDK: http://cloud.google.com/sdk


If you're running your application elsewhere
--------------------------------------------

If you are running the application elsewhere, you probably
need a `service account`_ JSON keyfile.

In production, we recommend that the contents of this file
be provided as an environment variable (`12 Factor App`_)
so credentials are not part of your source code.

Service account info (recommended)
``````````````````````````````````

If you have the service account info as a dictionary, that
can be used to connect to datastore

.. code-block:: python

    from gcloud_odm import connection
    connection.connect_with_account_info(info_dict)

If you have this as a JSON dump in environment (if you use
heroku for example)

By default, the environment variable
`GOOGLE_APPLICATION_CREDENTIALS_INFO` is understood by the conenction.


.. code-block:: python

    from gcloud_odm import connection
    connection.connect_with_account_info()


Alternatively, if you have a different environment variable,
you can manually load the JSON and then pass the dictionary
to the `connect_with_account_info` method.

.. code-block:: python

    from gcloud_odm import connection
    info_dict = json.loads(os.environ['CREDS'])
    connection.connect_with_account_info(info_dict)


If you have a JSON keyfile
``````````````````````````

.. code-block:: python

    from gcloud_odm import connection
    connection.connect_with_account_file('/path/to/keyfile.json')

or, if the file is specified in the environment variable

.. code-block:: bash

    $ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"

.. code-block:: python

    from gcloud_odm import connection
    # Call without an argument
    # and the environment variable's value is looked up
    connection.connect_with_account_file()

.. _service account: https://cloud.google.com/storage/docs/authentication#generating-a-private-key


Setting project and namespace
=============================

.. code-block:: python

    from gcloud_odm import connection
    connection.project = 'hello-world'
    connection.namespace = 'default'


More information on authentication
==================================

Read more about the `authentication system`_ in the python library.

.. _authentication system: https://googlecloudplatform.github.io/google-cloud-python/stable/google-cloud-auth.html
.. _Precedence:

Credential Discovery Precedence
-------------------------------

If there is no explicit connection, using `connect_with_account_file`
or `connect_with_account_info`, the connection is inferred from
environment variables.

1. Look for `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
2. Look for `GOOGLE_APPLICATION_CREDENTIALS_INFO` environment variable.
3. Assume no explicit credentials are needed (local dev or app engine).
