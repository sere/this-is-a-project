# -*- coding: utf-8 -*-
#
# Abstraction of the connection between two Node objects
#
# FIXME: this is still part of the locator.py horror, is there
#        a better way of doing this?
from locator import Base
from sqlalchemy import Column, Integer, String

class Connection(Base):
    __tablename__ = 'connection'

    # Multiple definitions of the primary_key attribute as True,
    # in the sqlite dialect, make a composite primary key, which
    # is what we want here
    id1 = Column(String, primary_key=True)
    id2 = Column(String, primary_key=True)
    class1 = Column(String)
    class2 = Column(String)

    def __init__(self, id1, id2, class1, class2):
        assert(id1 != None and id2 != None)
        assert(class1 != None and class2 != None)
        self.id1 = id1
        self.id2 = id2
        self.class1 = class1
        self.class2 = class2

    def get_id(self):
        return (self.id1, self.id2)

    def get_class(self):
        return (self.class1, self.class2)

# vim: set et sts=4 sw=4:
