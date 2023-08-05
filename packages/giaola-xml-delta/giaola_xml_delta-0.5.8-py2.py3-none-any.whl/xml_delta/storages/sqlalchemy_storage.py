#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Storage
from models import Base, Listing


class SqlAlchemyStorage(Storage):

    def fetch_listings(self, ids):
        results = self.session.query(Listing).filter(Listing.dasUniqueId.in_(ids),
                                                     Listing.type == self.type).all()
        return [result.to_dict() for result in results]

    def cleanup(self):
        self.session.query(Listing).filter(Listing.type == self.type).delete()
        self.session.commit()

    def count(self):
        return self.session.query(Listing).filter(Listing.type == self.type).count()

    def fetch_errors(self):
        return self.session.query(Listing).filter(Listing.type == self.type,
                                                  Listing.sent == False)

    def bulk_create(self, data, network_errors={}):
        db_objects = []
        for key, value in data.iteritems():
            sent = not network_errors.has_key(key)
            db_objects.append(Listing(dasUniqueId=key,
                                      type=self.type,
                                      data=value,
                                      sent=sent))
        self.session.bulk_save_objects(db_objects)
        self.session.commit()

    def bulk_update(self, data, network_errors={}):
        for key, value in data.iteritems():
            sent = not network_errors.has_key(key)
            model = Listing(dasUniqueId=key,
                            type=self.type,
                            data=value,
                            sent=sent)
            self.session.merge(model)

        self.session.commit()

    def _connect(self):
        # engine = create_engine(self.connection_string, echo=True, client_encoding='utf8')
        engine = create_engine(self.connection_string)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        self.session = Session()
