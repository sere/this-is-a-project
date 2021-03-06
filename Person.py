# -*- coding: utf-8 -*-
#
# Abstraction of a Person in a network
#
from Node import *
from locator import Base
if Base != object.__class__:
    from sqlalchemy import Column, Integer, String

class Person(Node, Base):
    if Base != object.__class__:
        __tablename__ = 'person'
        ident = Column(String, primary_key=True)
        name = Column(String)
        surname = Column(String)
        x = Column(Integer)
        y = Column(Integer)

    read_features = ["name", "surname"]
    features = ["name", "surname"]
    
    tiny_pixbuf = gtk.gdk.pixbuf_new_from_xpm_data([
        "26 26 5 1",
        "  c black",
        ". c grey",
        "o c yellow",
        "X c blue",
        "- c None",
        "--------------------------",
        "------------  ------------",
        "----------  oo  ----------",
        "--------- oooooo ---------",
        "--------  o oo o  --------",
        "--------  oooooo  --------",
        "--------   oooo   --------",
        "------------oo------------",
        "------------oo------------",
        "--ooXXXXXXXXXXXXXXXXXXoo--",
        "---oXXXXXXXXXXXXXXXXXXo---",
        "----------XXXXXX----------",
        "----------XXXXXX----------",
        "----------XXXXXX----------",
        "----------XXXXXX----------",
        "----------XXXXXX----------",
        "----------      ----------",
        "----------      ----------",
        "---------        ---------",
        "--------          --------",
        "--------    --    --------",
        "-------    ----    -------",
        "-------    ----    -------",
        "------    ------    ------",
        "-----    --------    -----",
        "--------------------------"
        ])

    def __init__(self, name=None, surname='8', x=50, y=50, ident=None, gui=None):
        Node.__init__(self, name, 'Person', x, y, ident, gui)
        self.surname = surname
        self.find_neighbors_script = "./script.sh"

    def node_clicked(self, widget, event):
        # TODO
        # If right-click
        if event.button == 3:
            newmenu = gtk.Menu()
            newitem = gtk.MenuItem('Find people')
            newmenu.append(newitem)
            newitem.connect("button-press-event", self.find_neighbors, )
            newitem1 = gtk.MenuItem('Find pc')
            newmenu.append(newitem1)
            newitem2 = gtk.MenuItem('Find DNS')
            newmenu.append(newitem2)
            item_remove = gtk.MenuItem('Remove')
            newmenu.append(item_remove)
            item_remove.connect("button-press-event", self.disappear)
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
                    neigh = self.gui.get_new_node(classname, "surname", newid, self.x, self.y)
                self.gui.connect(self, neigh)

# vim: set et sts=4 sw=4:

