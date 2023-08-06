#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Werkzeug',
    'schematics',
    'google-cloud-datastore',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='gcloud_odm',
    version='0.0.4',
    description="Google cloud datastore based ODM",
    long_description=readme + '\n\n' + history,
    author="Fulfil.io Inc.",
    author_email='support@fulfil.io',
    url='https://github.com/fulfilio/gcloud_odm',
    packages=find_packages(exclude=("tests", "tests.*",)),
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='gcloud_odm',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
