#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import Column, String, Integer, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


def update_updated_count(context):
    count = context.current_parameters['updated_count'] or 0
    return count + 1

class Listing(Base):
    __tablename__ = 'listing'

    dasUniqueId = Column(String(20), primary_key=True)
    type = Column(String(20), primary_key=True)
    data = Column(JSON)


    sent = Column(Boolean, default=False)

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Change(id='%s', updated_count='%s')>" % (self.dasUniqueId, self.updated_count)

    def to_dict(self):
        return dict(**self.data)
