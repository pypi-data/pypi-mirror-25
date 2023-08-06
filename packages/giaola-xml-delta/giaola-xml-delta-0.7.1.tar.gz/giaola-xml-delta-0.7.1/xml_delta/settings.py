#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from os import environ

from utils import string_2_bool

# Network settings
NETWORK_CLASS = environ.get('DELTA_NETWORK_CLASS', 'xml_delta.network.Rest')
NETWORK_RETRIES = environ.get('DELTA_NETWORK_RETRIES', 0)
NETWORK_CONNECTION_TIMEOUT = int(environ.get('DELTA_NETWORK_CONNECTION_TIMEOUT', 5))  # seconds

# Storage settings
STORAGE_CLASS = environ.get('DELTA_STORAGE_CLASS', 'xml_delta.storages.SqlAlchemyStorage')
STORAGE_DATABASE_URL = environ.get('DELTA_STORAGE_DATABASE_URL',
                                   'mysql+cymysql://delta:delta@localhost:3306/delta')

# Parser settings
PARSER_CLASS = environ.get('DELTA_PARSER_CLASS', 'xml_delta.parsers.XMLToDictParser')
PARSER_FLUSH_COUNTER = int(environ.get('DELTA_PARSER_FLUSH_COUNTER', 100))

# Delta settings
DELTA_CLASS = environ.get('DELTA_DELTA_CLASS', 'xml_delta.delta.JsonDelta')

# logging

LOGGING = {
    'version': 1,
    'handlers': {
        'root': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(name)s:%(funcName)s(%(lineno)3d): %(message)s'
        },
    }
}
#
logging.basicConfig(**LOGGING)

# Watcher settings
WATCHER_CLASS = environ.get('DELTA_WATCHER_CLASS', 'xml_delta.watchers.FileSystemHandler')
