#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml_delta.core import Observable


class Network:

    def __init__(self,
                 enabled=True,
                 endpoint=None,
                 headers=None,
                 retries=0,
                 timeout=5):
        self.enabled = enabled
        self.endpoint = endpoint
        self.headers = headers
        self.retries = retries
        self.timeout = timeout

    def send(self, data, *args, **kwargs):
        raise NotImplemented()
