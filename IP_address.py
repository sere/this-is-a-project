# -*- coding: utf-8 -*-
#
# Representation of an IP address
#
from Node import *
from locator import Base
if Base != object.__class__:
    from sqlalchemy import Column, Integer, String

class IP_address(Node, Base):
    if Base != object.__class__:
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


    def __init__(self, name=None, ip="192.168.0.2", x=50, y=50, ident=None, gui=None):
        assert(ip != None)
        self.ip = ip
	Node.__init__(self, name, 'IP', x, y, ident, gui)

    def getIp(self):
        return self.ip

    def setIp(self, ip):
        assert(ip != None)
        self.ip = ip

# this doesn't have to find neighbors
    def node_clicked(self, widget, event):
        # If right-click
        if event.button == 3:
            if not self.gui.node_connected_with_class(self, "Host") and not self.gui.node_connected_with_class(self, "DNS_server"):
                newmenu = gtk.Menu()
                item_remove = gtk.MenuItem('Remove')
                newmenu.append(item_remove)
                item_remove.connect("button-press-event", self.disappear)
                newmenu.show_all()
                newmenu.popup(None, None, None, event.button, event.time)

# vim: set et sts=4 sw=4:
