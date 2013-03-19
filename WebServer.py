# -*- coding: utf-8 -*-
#
# A most important resource in a network
#
from Node import *
from Host import *

class WebServer(Node):

    features = ["name"]
    
    tiny_pixbuf = gtk.gdk.pixbuf_new_from_xpm_data([
        "26 26 5 1",
        "  c black",
        ". c grey",
        "o c yellow",
        "X c blue",
        "- c None",
        "--------------------------",
        "--------------------------",
        "--XXXX----XXX----X-----X--",
        "-X--------X--X---X-----X--",
        "-X--------X---X--X-----X--",
        "--XXX-----XXX-----X---X---",
        "------X---X--X----X---X---",
        "------X---X---X----X-X----",
        "-XXXXX----X---X-----X-----",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------",
        "--------------------------"
        ])

    def __init__(self, name=None, Type='data',  x=50, y=50, ident=None, gui=None):
        assert(name != None)
        self.name=name
        Node.__init__(self, name,'webserver', x, y, ident, gui)
        self.find_neighbors_script = "./script.sh"

    def node_clicked(self, widget, event):
        # TODO
        # If right-click
        if event.button == 3:
            newmenu = gtk.Menu()
            newitem = gtk.MenuItem('stub')
            newmenu.append(newitem)
            newitem.connect("button-press-event", self.find_neighbors, )
            newitem1 = gtk.MenuItem('stub')
            newmenu.append(newitem1)
            newmenu.show_all()
            newmenu.popup(None, None, None, event.button, event.time)

    def find_neighbors(self, widget, event):
        # TODO
        # Do something useful and rational, like searching for some
        # specific method of the class. By now just fire the execution
        # of a script and read the result. We assume by now that the
        # output has already been filtered and contains only the id
        # of the neighbor.
        out = self.runProcess([self.find_neighbors_script])
        for newid in str(out).strip().split():
                neigh = self.gui.search_for_node("surname", newid)
                if neigh == None:
                    classname = self.__class__.__name__
                    neigh = self.gui.get_new_node(classname, "surname", newid)
                self.gui.connect(self, neigh)

# vim: set et sts=4 sw=4:

