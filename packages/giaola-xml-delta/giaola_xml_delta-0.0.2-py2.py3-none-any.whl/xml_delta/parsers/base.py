#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml_delta.core import Observable

class Parser(Observable):
    EVENT_FLUSHED = 'parser:flush'

    def __init__(self, flush_counter=1):
        super(Parser, self).__init__()
        self.flush_counter = flush_counter

    def parse(self, **kwargs):
        raise NotImplemented()

    def _fire_if_needed(self, payload, force=False):
        if len(self.data) == self.flush_counter or (force and len(self.data) > 0):
            self.fire(self.EVENT_FLUSHED, payload=self.data)
            self.data = []
