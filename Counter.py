# -*- coding: utf-8 -*-
#
# Counter class which handles generation of unique identifiers for resources
#
import thread

class Counter:

    count = 0
    lock = None

    def __init__(self, init=0):
        self.count = init
        self.lock = thread.allocate_lock()

    def get(self):
        self.lock.acquire()
        self.count = self.count + 1
        self.lock.release()
        return self.count

    def put(self):
        self.lock.acquire()
        self.count = self.count - 1
        self.lock.release()
        return self.count

# vim: set et sts=4 sw=4:
