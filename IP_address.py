# -*- coding: utf-8 -*-
#
# Representation of a host
#
from Node import *
from locator import Base
from sqlalchemy import Column, Integer, String

class IP_address(Node):
    __tablename__ = 'ipaddr'

    ident = Column(String, primary_key=True)
    name = Column(String)
    ip = Column(String)
    x = Column(Integer)
    y = Column(Integer)

    read_features = ["ip"]
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
