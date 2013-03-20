# -*- coding: utf-8 -*-
#
# Representation of a host
#
from Node import *

class DNS_server(Node):

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


    def __init__(self, ipaddr=None, name=None, Type='Data', x=50, y=50, ident=None, gui=None):
        assert(ipaddr != None)
        self.ip = ipaddr.getIp()
	Node.__init__(self, name, Type, x, y, ident, gui)
	self.find_neighbors_script = "./script.sh"

    def node_clicked(self, widget, event):
        # TODO modify
        # If right-click
        if event.button == 3:
            newmenu = gtk.Menu()
            newitem = gtk.MenuItem('Find neighbors')
            newmenu.append(newitem)
            newitem.connect("button-press-event", self.find_neighbors)
            newitem1 = gtk.MenuItem('Item 2')
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
