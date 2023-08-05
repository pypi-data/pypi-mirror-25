#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging

import requests

from .base import Network

logger = logging.getLogger(__name__)

class Rest(Network):

    def send(self, data, *args, **kwargs):
        if not self.enabled:
            return { key : 'Network.Enabled=False' for key in data }

        network_errors = {}
        for key, value in data.iteritems():
            try:
                json_value = json.dumps(value)
                response = requests.post(self.endpoint,
                                         data=json_value,
                                         headers=self.headers,
                                         timeout=self.timeout)
                if not response.status_code == 200:
                    network_errors[key] = response.status_code
            except Exception as err:
                network_errors[key] = err.message
                pass


        return network_errors
