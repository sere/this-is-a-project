# -*- coding: utf-8 -*-
#
# Abstraction of a WebServer
#
from Node import *
from Host import *
from locator import Base
if Base != None:
    from sqlalchemy import Column, Integer, String

class WebServer(Node):
    if Base != None:
        __tablename__ = 'webserver'
        ident = Column(String, primary_key=True)
        name = Column(String)
        x = Column(Integer)
        y = Column(Integer)

    read_features = ["name", "host"]
    features = ["name", "host"]

    tiny_pixbuf = gtk.gdk.pixbuf_new_from_xpm_data([
        "26 26 5 1",
        "  c black",
        ". c grey",
        "o c yellow",
        "X c blue",
        "- c None",
        "--------------------------",
        "--------------------------",
        "-w--w-w--w-wwwww--wwww----",
        "-w--w-w--w-w------w---w---",
        "-w--w-w--w-w------w---w---",
        "--w--w--w--wwww---wwww----",
        "--w--w--w--w------w---w---",
        "--w--w--w--w------w---w---",
        "---ww-ww---wwwww--wwww----",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--wwww----www----w-----w--",
        "-w--------w--w---w-----w--",
        "-w--------w---w--w-----w--",
        "--www-----www-----w---w---",
        "------w---w--w----w---w---",
        "------w---w---w----w-w----",
        "-wwwww----w---w-----w-----",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------"
        ])

    def __init__(self, name=None, host=None, x=50, y=50, ident=None, gui=None):
        assert(name != None)
        Node.__init__(self, name, 'WebServer', x, y, ident, gui)
        self.name=name
        if host == None:
            host = gui.get_new_node("Host", None, None, x - 30, y)
            gui.connect(self, host)
        assert(host != None)
        self.host=host
        self.find_neighbors_script = "./script.sh"

    def node_clicked(self, widget, event):
        # TODO modify
        # If right-click
        if event.button == 3:
            newmenu = gtk.Menu()
            newitem = gtk.MenuItem('Find neighbors')
            newmenu.append(newitem)
            newitem.connect("button-press-event", self.find_neighbors)
            newmenu.show_all()
            newmenu.popup(None, None, None, event.button, event.time)

    def find_connect_node(self, newid):
        # Create new webserver
        classname = self.__class__.__name__
        neigh = self.gui.search_for_node_with_class(classname, "name", newid)
        if neigh == None:
            # Create a new WebServer instance
            neigh = self.gui.get_new_node(classname, "name", newid, self.x, self.y)
        self.gui.connect(self, neigh)

    # Find webservers by name
    def find_neighbors(self, widget, event):
        out = self.runProcess([self.find_neighbors_script])
        for newid in str(out).strip().split():
            self.find_connect_node(newid)

# vim: set et sts=4 sw=4:

