# -*- coding: utf-8 -*-
"""
    contrib.flask

    :license: see LICENSE for details.
"""
import json

from gcloud_odm.datastore_client import connection


class GCloudODM(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        if 'GCLOUD_PROJECT' in app.config:
            connection.project = app.config.get('GCLOUD_PROJECT')
        if 'GCLOUD_ODM_NAMESPACE' in app.config:
            connection.namespace = app.config.get('GCLOUD_ODM_NAMESPACE')

        if app.config.get('GOOGLE_APPLICATION_CREDENTIALS_INFO'):
            connection.connect_with_account_info(json.loads(
                app.config.get('GOOGLE_APPLICATION_CREDENTIALS_INFO')))
        elif app.config.get('GOOGLE_APPLICATION_CREDENTIALS'):
            connection.connect_with_account_file(
                app.config.get('GOOGLE_APPLICATION_CREDENTIALS'))
