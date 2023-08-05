#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml_delta.core import Observable


class Storage(Observable):
    EVENT_READ = 'storage:read'

    def __init__(self,  connection, type):
        super(Storage, self).__init__()
        self.connection_string = connection
        self.type = type
        self._connect()

    def fetch_listings(self, ids):
        raise NotImplemented()

    def bulk_create(self, data, network_errors=None):
        raise NotImplemented()

    def bulk_update(self, data, network_errors=None):
        raise NotImplemented()

    def _connect(self):
        raise NotImplemented()
