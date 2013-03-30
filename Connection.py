# -*- coding: utf-8 -*-
#
# Abstraction of the connection between two Node objects
#

class Connection:

    id1 = None
    id2 = None
    class1 = None
    class2 = None

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
