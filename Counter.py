# -*- coding: utf-8 -*-
#
# Counter class which handles generation of unique identifiers for resources
#

class Counter:

    count = 0

    def __init__(self, init=0):
        self.count = init

    def get(self):
        self.count = self.count + 1
        return self.count

    def put(self):
        self.count = self.count - 1
        return self.count

# vim: set et sts=4 sw=4:
