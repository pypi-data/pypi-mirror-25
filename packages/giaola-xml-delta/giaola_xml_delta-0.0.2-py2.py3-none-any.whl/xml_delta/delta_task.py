# -*- coding: utf-8 -*-

"""Main module."""
import time

import logging

import settings
from utils import load_class

logger = logging.getLogger(__name__)

class DeltaTask(object):

    total_parsed = 0

    def __init__(self, type, file, tag, pk, endpoint=None):
        self.type = type
        self.file_path = file
        self.tag = tag
        self.pk = pk
        self.endpoint = endpoint

    def execute(self):
        # print("*" * 40)
        # print("Delta task starting")
        # print("type : {0}".format(self.type))
        # print("tag : {0}".format(self.tag))
        # print("pk : {0}".format(self.pk))
        # print("type : {0}".format(self.type))
        # if self.endpoint:
        #     print("endpoint : {0}".format(self.endpoint))
        #
        # print("...")

        self.start = time.time()

        try:
            Parser = load_class(settings.PARSER_CLASS)
            Storage = load_class(settings.STORAGE_CLASS)
            Delta = load_class(settings.DELTA_CLASS)
            Network = load_class(settings.NETWORK_CLASS)

            if self.file_path:

                self.parser = Parser(flush_counter=settings.PARSER_FLUSH_COUNTER)

                self.parser.subscribe(Parser.EVENT_FLUSHED, self.handle_parser_flushed)

                self.storage = Storage(connection=settings.STORAGE_DATABASE_URL, type=self.type)

                self.delta = Delta()

                network_enabled = self.endpoint or False
                self.network = Network(network_enabled,
                                       self.endpoint,
                                       {},
                                       settings.NETWORK_RETRIES,
                                       settings.NETWORK_CONNECTION_TIMEOUT)

                self.parser.parse(self.file_path, self.tag)

        except Exception, e:
            logger.exception(e)

        # print("time elapsed : {0}".format(time.time() - self.start))
        # print("*" * 40)
        # print("\n")

    def handle_parser_flushed(self, event):
        ids = [record[self.pk] for record in event.payload]

        db_listings = self.storage.fetch_listings(ids)

        to_create, to_update = self.delta.diff(self.pk, db_listings, event.payload)

        network_errors = self.network.send(to_create)
        self.storage.bulk_create(to_create, network_errors)

        network_errors = self.network.send(to_update)
        self.storage.bulk_update(to_update, network_errors)
