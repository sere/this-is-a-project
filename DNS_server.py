# -*- coding: utf-8 -*-
#
# Abstraction of a DNS server
#
from Node import *
from locator import Base
if Base != object.__class__:
    from sqlalchemy import Column, Integer, String

class DNS_server(Node, Base):
    if Base != object.__class__:
        __tablename__ = 'dns_server'
        ident = Column(String, primary_key=True)
        name = Column(String)
        x = Column(Integer)
        y = Column(Integer)

    read_features = ["name", "ip"]
    features = ["name", "ip"]

    tiny_pixbuf = gtk.gdk.pixbuf_new_from_xpm_data([
        "26 20 5 1",
        "  c black",
        ". c grey",
        "o c yellow",
        "X c blue",
        "- c None",
        "--------------------------",
        "-........................-",
        "-........................-",
        "-..XXXXXXXXXXXXXXXXXXXX..-",
        "-..XXooXXXoXXXXoXXooooX..-",
        "-..XXoXoXXooXXXoXoXXXXX..-",
        "-..XXoXXoXoXoXXoXXooXXX..-",
        "-..XXoXXoXoXXoXoXXXXXoX..-",
        "-..XXoXoXXoXXXooXXXXXoX..-",
        "-..XXooXXXoXXXXoXooooXX..-",
        "-..XXXXXXXXXXXXXXXXXXXX..-",
        "-........................-",
        "-........................-",
        "---------........---------",
        "--------..........--------",
        "---....................---",
        "---. . . . . . . . . ..---",
        "---                    ---",
        "---. . . . . . . . . . ---",
        "---                    ---",
        "---. . . . . . . . . ..---"
        ])


    def __init__(self, ipaddr=None, name=None, x=50, y=50, ident=None, gui=None):
        assert(name != None)
	Node.__init__(self, name, "DNS server", x, y, ident, gui)
        if ipaddr == None:
            ipaddr = gui.get_new_node("IP_address", None, None, x - 30, y)
            gui.connect(self, ipaddr)
        assert(ipaddr != None)
        self.ip = ipaddr.getIp()
	self.find_neighbors_script = "./script.sh"

    def node_clicked(self, widget, event):
        # If right-click
        if event.button == 3:
            newmenu = gtk.Menu()
            newitem = gtk.MenuItem('Find neighbors')
            newmenu.append(newitem)
            newitem.connect("button-press-event", self.find_neighbors)
            newmenu.show_all()
            newmenu.popup(None, None, None, event.button, event.time)

    def find_connect_node(self, newid):
        # Create new DNS server
        classname = self.__class__.__name__
        neigh = self.gui.search_for_node_with_class(classname, "name", newid)
        if neigh == None:
            # Create a new DNS server instance
            neigh = self.gui.get_new_node(classname, "name", newid, self.x, self.y)
        self.gui.connect(self, neigh)

    def find_neighbors(self, widget, event):
        out = self.runProcess([self.find_neighbors_script])
        for newid in str(out).strip().split():
            self.find_connect_node(newid)
 
# vim: set et sts=4 sw=4:
