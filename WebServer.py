# -*- coding: utf-8 -*-
#
# A most important resource in a network
#
from Node import *
from Host import *

class WebServer(Node):

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

    def __init__(self, name=None, Type='data', host=None, x=50, y=50, ident=None, gui=None):
        assert(name != None)
        self.name=name
        assert(host != None)
        self.host=host
        Node.__init__(self, name,'webserver', x, y, ident, gui)
        self.find_neighbors_script = "./script.sh"

    def node_clicked(self, widget, event):
        # TODO modify
        # If right-click
        if event.button == 3:
            newmenu = gtk.Menu()
            newitem = gtk.MenuItem('Find neighbors')
            newmenu.append(newitem)
            newitem.connect("button-press-event", self.find_neighbors, )
            newitem1 = gtk.MenuItem('item 2')
            newmenu.append(newitem1)
            newmenu.show_all()
            newmenu.popup(None, None, None, event.button, event.time)

    def find_neighbors(self, widget, event):
        # TODO modify
        # Do something useful and rational, like searching for some
        # specific method of the class. By now just fire the execution
        # of a script and read the result. We assume by now that the
        # output has already been filtered and contains only the id
        # of the neighbor.
        out = self.runProcess([self.find_neighbors_script])
        for newid in str(out).strip().split():
                neigh = self.gui.search_for_node("ident", newid)
                if neigh == None:
                    classname = self.__class__.__name__
                    neigh = self.gui.get_new_node(classname, "ident", newid)
                self.gui.connect(self, neigh)

# vim: set et sts=4 sw=4:

