#!/usr/bin/env python
# -*- coding: utf-8 -*-



from .base import Delta

import json

import xml_delta.echo as echo

import logging
logger = logging.getLogger(__name__)

class JsonDelta(Delta):
    def diff(self, pk, old_data, new_data, *args, **kwargs):
        old_data = {k.get(pk): k for k in old_data}
        new_data = {k.get(pk): k for k in new_data}

        to_update = {}
        to_create = {}

        for k, new in new_data.items():
            old = old_data.get(k)
            if not old:
                echo.echo("Item with id = {0} has been inserted.".format(k))
                to_create[k] = new
            else:
                if not sorted(old.items()) == sorted(new.items()):

                    echo.echo("Item with id {0} has changed.".format(k))
                    to_update[k] = new

        return to_create, to_update
