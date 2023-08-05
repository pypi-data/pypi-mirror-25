#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from watchdog.observers import Observer

from watchdog.events import RegexMatchingEventHandler

from xml_delta import DeltaTask

class RegexWatcher:

    def __init__(self, path, prefix, **kwargs):
        self.path = path
        self.prefix = prefix
        self.task_args = kwargs

    def start(self):
        self.observer = Observer()
        self.event_handler = RegexEventHandler(self.prefix, **self.task_args)

        self.observer.schedule(self.event_handler, self.path)
        self.observer.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.observer.stop()
                break

        self.observer.join()

        print("Watched Finished")

    def stop(self):
        self.observer.stop()
        self.observer.join()

class RegexEventHandler(RegexMatchingEventHandler):

    def __init__(self, prefix, **kwargs):
        regex = r".*{0}.*\.xml".format(prefix)
        self.task_args = kwargs
        super(RegexEventHandler, self).__init__(regexes=[regex],
                                                ignore_directories=True)

    def on_created(self, event):
        delta_task = DeltaTask(file=event.src_path, **self.task_args)
        delta_task.execute()




