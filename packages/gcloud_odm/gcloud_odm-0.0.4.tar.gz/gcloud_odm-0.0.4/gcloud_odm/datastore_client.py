# -*- coding: utf-8 -*-
"""
    datastore_client

    :license: see LICENSE for details.
"""
import os
import json
from datetime import datetime

from google.cloud import datastore
from google.oauth2.service_account import Credentials
from google.auth.exceptions import DefaultCredentialsError
from werkzeug.local import LocalProxy


class Connection(object):
    _instance = None
    client = None
    _project = None
    _namespace = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self, credentials=None):
        if credentials is not None:
            self.credentials = credentials
        else:
            try:
                self.discover_credentials()
            except DefaultCredentialsError:
                pass
        self.refresh_datastore_client(silent=True)

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        self._project = value
        self.refresh_datastore_client(silent=True)

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = value
        self.refresh_datastore_client(silent=True)

    def get_client(self, buffer_seconds=60):
        client_expiry = self.client and self.client._credentials.expiry
        if self.client is None or (client_expiry and (
                client_expiry - datetime.utcnow()).total_seconds() <
                buffer_seconds):
            # If not client or token is about to expire in 1 min.
            # client_expiry can be None when oauth credentials are not
            # generated in client. Credentials are only generated on 1st
            # use.
            self.refresh_datastore_client()
        return self.client

    def refresh_datastore_client(self, silent=False):
        """
        Return an authenticated instance of google datastore
        """
        try:
            self.client = datastore.Client(
                credentials=self.credentials,
                project=self.project,
                namespace=self.namespace
            )
        except DefaultCredentialsError:
            if not silent:
                raise

    def connect_with_account_info(self, info=None):
        key = 'GOOGLE_APPLICATION_CREDENTIALS_INFO'

        if info is None and key not in os.environ:
            message = '\n'.join([
                "Credentials not found.",
                "info can be passed as a dictionary or "
                "%s environment variable with a json "
                "dump should be specified" % (key,),
                "Link Here"
            ])
            raise Exception(message)

        if info is None:
            info = json.loads(os.environ[key])

        self.credentials = Credentials.from_service_account_info(info)
        self.refresh_datastore_client()

    def connect_with_account_file(self, filename=None):
        key = 'GOOGLE_APPLICATION_CREDENTIALS'

        if filename is None and key not in os.environ:
            message = '\n'.join([
                "Credentials not found.",
                "filename can be passed as an argument or "
                "%s environment variable with the "
                "filename should be specified" % (key,),
                "Link Here"
            ])
            raise Exception(message)

        self.credentials = Credentials.from_service_account_file(
            filename or os.environ[key]
        )

    def discover_credentials(self):
        "Try and discover authentication from env vars"
        if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
            self.connect_with_account_file()
        elif 'GOOGLE_APPLICATION_CREDENTIALS_INFO' in os.environ:
            self.connect_with_account_info()
        else:
            self.credentials = None


connection = Connection()
client = LocalProxy(connection.get_client)
