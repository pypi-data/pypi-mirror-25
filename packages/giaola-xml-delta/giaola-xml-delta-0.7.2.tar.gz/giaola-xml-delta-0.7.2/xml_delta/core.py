#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread
import logging


logger = logging.getLogger(__name__)


class Event(object):
    pass

class Observable(object):
    def __init__(self, workers=5):
        self.callbacks = {}
        self.queue = Queue()

        for i in range(workers):
            t = Thread(target=self.__worker)
            t.daemon = True
            t.start()

    def __worker(self):
        while True:
            thread_kwargs = self.queue.get()

            try:
                thread_kwargs['target'](*thread_kwargs['args'])
            except Exception as e:
                logger.exception(e)

            self.queue.task_done()

    def subscribe(self, event, callback):
        self.callbacks[event] = self.callbacks.get(event, [])
        self.callbacks[event].append(callback)

    def fire(self, event, **attrs):
        e = Event()
        e.source = self
        e.name = event

        for k, v in attrs.iteritems():
            setattr(e, k, v)

        for fn in self.callbacks.get(event, []):
            self.queue.put({'target': fn, 'args': (e,)})

        self.queue.join()
