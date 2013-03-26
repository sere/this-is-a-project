# -*- coding: utf-8 -*-
#
# Abstraction of the connection between two Node objects
#

class Connection:

    id1 = None
    id2 = None

    def __init__(self, id1, id2):
        assert(id1 != None and id2 != None)
        self.id1 = id1
        self.id2 = id2

# vim: set et sts=4 sw=4:
