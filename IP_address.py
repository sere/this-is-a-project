# -*- coding: utf-8 -*-
#
# Representation of a host
#
from Node import *

class IP_address(Node):

    features = []

    tiny_pixbuf = gtk.gdk.pixbuf_new_from_xpm_data([
        "26 20 5 1",
        "  c black",
        ". c grey",
        "o c yellow",
        "X c blue",
        "- c None",
        "--------------------------",
        "--------------------------",
        "-    -----             ---",
        "-    -----    ------    --",
        "-    -----    --------   -",
        "-    -----    --------   -",
        "-    -----    --------   -",
        "-    -----    --------   -",
        "-    -----    --------   -",
        "-    -----    -------    -",
        "-    -----             ---",
        "-    -----    ------------",
        "-    -----    ------------",
        "-    -----    ------------",
        "-    -----    ------------",
        "-    -----    ------------",
        "-    -----    ------------",
        "-    -----    ------------",
        "-    -----    ------------",
        "--------------------------",
        "--------------------------",
        ])


    def __init__(self, name=None, ip="192.168.0.2", Type='IP', x=50, y=50, ident=None, gui=None):
        self.ip = ip
        assert(ip != None)
	Node.__init__(self, name, Type, x, y, ident, gui)

    def getIp(self):
        return self.ip

    def setIp(self, ip):
        assert(ip != None)
        self.ip = ip

# this doesn't have to find neighbors

# vim: set et sts=4 sw=4:
