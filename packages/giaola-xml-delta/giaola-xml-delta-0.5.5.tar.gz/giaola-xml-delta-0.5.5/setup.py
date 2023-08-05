#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click==6.7',
    'SQLAlchemy==1.1',
    'psycopg2==2.7',
    'requests==2.18',
    'watchdog==0.8',
    'lxml==3.8.0',
    'SQLAlchemy-Paginator==0.1',
]

setup(
    # Package Name
    name='giaola-xml-delta',

    # Version
    version='0.5.5',

    description="Package to find differences between big xml files.",
    long_description=readme + '\n\n' + history,

    author="Dimitris Klouvas | Marsel Tzatzo",
    author_email='tmarselg@gmail.com',

    url='https://bitbucket.org/giaola/11888_delta',

    # Packages to be deployed
    packages=find_packages(exclude=['compose', 'data', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'xml_delta=xml_delta.cli:xml_delta',
            'xml_delta_watcher=xml_delta.cli:xml_delta_watcher',
            'xml_delta_check_network=xml_delta.cli:check_network',
            'xml_delta_cleanup=xml_delta.cli:cleanup_type',
            'xml_delta_count=xml_delta.cli:count_type',
            'xml_delta_errors=xml_delta.cli:errors',
            'xml_delta_errors_count=xml_delta.cli:errors_count',
            'xml_delta_errors_sync=xml_delta.cli:errors_sync',
        ]
    },

    install_requires=requirements,
    keywords='xml',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ]
)
