# -*- coding: utf-8 -*-
#
# A most important resource in a network
#
from Node import *

class Smiley(Node):

    read_features = ["name"]
    features = ["name"]

    tiny_pixbuf = gtk.gdk.pixbuf_new_from_xpm_data([
        "26 26 5 1",
        "  c black",
        ". c grey",
        "o c yellow",
        "X c blue",
        "- c None",
        "---------        ---------",
        "-------   oooooo   -------",
        "-----   oooooooooo   -----",
        "----  oooooooooooooo  ----",
        "---  oooooooooooooooo  ---",
        "--  oooooooooooooooooo  --",
        "-- oooooooooooooooooooo  -",
        "-  ooooooooooooooooooooo -",
        "- oooooooooooooooooooooo  ",
        "  ooooo   oooooo.    .ooo ",
        " ooooo XXX oooo. XXXX ooo ",
        " ooooo XXX oooo XXXXXX oo ",
        " ooooo. X .oooo XXXXXX oo ",
        " oooooo. .ooooo XXXXXX oo ",
        " oooooooooooooo. XXXX ooo ",
        " ooooooooooooooo.    .ooo ",
        "  ooooooooooooooooooooooo ",
        "- ooo.oooooooooooooooooo  ",
        "-  oo. .oooooooooo.  ooo -",
        "-- ooo   .ooooooo.  ooo  -",
        "--  ooo XX         .oo  --",
        "---  ooo  XXXXXXX .oo  ---",
        "----  oooo       ooo  ----",
        "-----   oooooooooo   -----",
        "------    oooooo    ------",
        "--------          --------"
        ])


    def __init__(self, name=None, Type='Data', x=50, y=50, ident=None, gui=None):
	Node.__init__(self, name, Type, x, y, ident, gui)
	self.find_neighbors_script = "./script.sh"

    def node_clicked(self, widget, event):
        # If right-click
        if event.button == 3:
            newmenu = gtk.Menu()
            newitem = gtk.MenuItem('Find friends!')
            newmenu.append(newitem)
            newitem.connect("button-press-event", self.find_neighbors)
            newmenu.show_all()
            newmenu.popup(None, None, None, event.button, event.time)

    def find_neighbors(self, widget, event):
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
