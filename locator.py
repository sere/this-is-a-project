#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# A resource locator which draws connected resources in a graph
#
import pygtk
pygtk.require('2.0')
import gtk
# FIXME: yes, this is horrible; yes, it must be fixed ASAP
import warnings
warnings.simplefilter('ignore', Warning)
import thread

try:
    import sqlalchemy
except ImportError:
    print "WARNING: no sqlalchemy library found.\n", \
          "The save/load features won't be available."
    # Define however the Base symbol so that all classes know that they
    # mustn't use the sqlalchemy features
    Base = object.__class__
else:
    from sqlalchemy.ext.declarative import declarative_base
    # FIXME: most horrible thing EVER, is there another way to do this?
    Base = declarative_base()
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

from Counter import *
from Connection import *
from Smiley import *
from Host import *
from Person import *
from IP_address import *
from WebServer import *
from DNS_server import *

MappedClasses = ["Smiley", "Host", "Person", \
                 "IP_address", "WebServer", \
                 "DNS_server"]

# Drag'n'Drop
TARGET_TYPE_NDDE = 80
toCanvas = [ ( "node_move", 0, TARGET_TYPE_NDDE ),]

class Locator:

    HEIGHT = 600
    WIDTH  = 600
    da = None
    style = None
    GC = None
    blackcolor = None

    def __init__(self, counter):
        self.NodeList = []
        self.Connections = []
        self.Connections_obj = []

        self.counter = counter
        self.lock = thread.allocate_lock()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_default_size(self.WIDTH, self.HEIGHT)
        window.set_title("Locator")
        window.connect("destroy", lambda w: gtk.main_quit())

        # HERE GOES ALL THE PACKING STUFF
        # Create vbox for main icon menu
        menu_vbox = gtk.VBox(False, 0)
        # FIXME: keep a list of known classes and generate buttons automatically
        button_host = gtk.Button(label="Host")
        button_host.connect("button-press-event", self.new_node_request, "Host")
        menu_vbox.pack_start(button_host, False, True, 5)
        button_host.show()
        if Base != object.__class__:
            # FIXME: use menu here?
            button_save = gtk.Button(label="Save")
            button_save.connect("button-press-event", self.save)
            menu_vbox.pack_start(button_save, False, True, 5)
            button_save.show()
            button_load = gtk.Button(label="Load")
            button_load.connect("button-press-event", self.load)
            menu_vbox.pack_start(button_load, False, True, 5)
            button_load.show()
        menu_vbox.show()
        # Create hbox for status
        status_hbox = gtk.HBox(False, 0)
        status_hbox.show()
        # Create right vbox for status and canvas
        right_vbox = gtk.VBox(False, 0)
        right_vbox.pack_start(self.makeLayout(), True, True, 0)
        right_vbox.pack_start(status_hbox, False, False, 0)
        right_vbox.show()
        main_hbox = gtk.HBox(False, 0)
        main_hbox.pack_start(menu_vbox, False, False, 0)
        main_hbox.pack_start(right_vbox, True, True, 0)
        main_hbox.show()

        window.add(main_hbox)
        window.show()

    def get_da(self):
        return self.da

    def layout_resize(self, widget, event):
        x, y, width, height = widget.get_allocation()
        if width > self.lwidth or height > self.lheight:
            self.lwidth = width
            self.lheight = height
            widget.set_size(self.lwidth, self.lheight)

    def makeLayout(self):
        self.lwidth = self.WIDTH
        self.lheight = self.HEIGHT
        self.da = gtk.DrawingArea()
        self.da.connect("expose-event",self.do_expose)
        self.da.show()

        table = gtk.Table(2, 2, False)
        table.show()
        layout = gtk.Layout()
        self.layout = layout
        layout.set_size(self.lwidth, self.lheight)
        layout.connect("size-allocate", self.layout_resize)
        layout.show()
        table.attach(layout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND,
                     gtk.FILL|gtk.EXPAND, 0, 0)

        # create the scrollbars and pack into the table
        vScrollbar = gtk.VScrollbar(None)
        vScrollbar.show()
        table.attach(vScrollbar, 1, 2, 0, 1, gtk.FILL|gtk.SHRINK,
                     gtk.FILL|gtk.SHRINK, 0, 0)
        hScrollbar = gtk.HScrollbar(None)
        hScrollbar.show()
        table.attach(hScrollbar, 0, 1, 1, 2, gtk.FILL|gtk.SHRINK,
                     gtk.FILL|gtk.SHRINK,
                     0, 0)
        table.attach(self.da, 1, 2, 1, 2, gtk.FILL|gtk.SHRINK,
                     gtk.FILL|gtk.SHRINK,
                     0, 0)

        # Tell the scrollbars to use the layout widget's adjustments
        vAdjust = layout.get_vadjustment()
        vScrollbar.set_adjustment(vAdjust)
        hAdjust = layout.get_hadjustment()
        hScrollbar.set_adjustment(hAdjust)

        # Drag'n'drop signals
        layout.connect("drag_data_received", self.receiveCallback)
        layout.drag_dest_set(gtk.DEST_DEFAULT_MOTION |
                                  gtk.DEST_DEFAULT_HIGHLIGHT |
                                  gtk.DEST_DEFAULT_DROP,
                                  toCanvas, gtk.gdk.ACTION_COPY)
        assert(table != None and layout != None)
        return table

    def do_expose(self, event, w):
        self.get_foreground_gc()
        self.draw_grid(20, self.lwidth, self.lheight)
        self.draw_connections()

    def receiveCallback(self, widget, context, x, y, selection, targetType,
                        time):
        if targetType == TARGET_TYPE_NDDE:
            node_id = int(selection.data)
            for node in self.NodeList :
                if id(node) == node_id :
                    node.move_on_layout(self.da, self.layout, x, y)

    def save(self, widget, event):
        # FIXME: let user choose the database name
        # FIXME: link the "echo" parameter to a "verbose" option
        # This operation is atomic, as the user may want to save different
        # graphs on different sqlite databases
        engine = create_engine('sqlite:///locator', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        # We assume that the two connection lists are equal in length
        # and that elements in the two lists correspond
        for c_id, c_ref in zip(self.Connections_obj, self.Connections):
            assert(c_ref[0].ident == c_id.id1 and c_ref[1].ident == c_id.id2)
            (node1, node2) = (c_ref[0], c_ref[1])
            print "Saving", node1.__repr__(), node2.__repr__()
            # Merge will create a new object or refresh the existing one;
            # this is more expensive, but will avoid exceptions
            session.merge(c_id)
            session.merge(c_ref[0])
            session.merge(c_ref[1])
        # Attempt a merge of all nodes to save also isolated ones
        for ref in self.NodeList:
            session.merge(ref)
        session.commit()
        session.close()

    def find_node_id(self, id):
        for node in self.NodeList:
            if node.ident == id:
                return node
        return None

    def load(self, widget, event):
        # FIXME: let user choose the database
        # FIXME: link the "echo" parameter to a "verbose" option
        # This operation is atomic, as the user may want to load different
        # graphs from different databases
        engine = create_engine('sqlite:///locator', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        del self.Connections[:]
        del self.Connections_obj[:]
        for node in self.NodeList:
            node.remove_layout(self.layout)
        del self.NodeList[:]
        for element in session.query(Connection).all():
            ident1 = element.get_id()[0]
            ident2 = element.get_id()[1]
            print "Loading", ident1, ident2
            class1 = element.get_class()[0]
            class2 = element.get_class()[1]
            self.Connections_obj.append(element)
            node1 = self.find_node_id(ident1)
            if node1 == None:
                element1 = eval("session.query(" + class1 + ").filter_by(ident=" + ident1 + ").first()")
                dict1 = element1.__dict__
                del dict1['_sa_instance_state']
                dict1["gui"] = self
            node2 = self.find_node_id(ident2)
            if node2 == None:
                element2 = eval("session.query(" + class2 + ").filter_by(ident=" + ident2 + ").first()")
                dict2 = element2.__dict__
                del dict2['_sa_instance_state']
                dict2["gui"] = self
            if node1 == None:
                # Handle priorities while instatiating nodes
                node1 = globals()[class1](**dict1)
                self.add_node(node1)
            if node2 == None:
                if self.has_priority_over(class1, class2):
                    key = None
                    if class1 == "IP_address":
                        key = "ipaddr"
                    else:
                        if class1 == "Host":
                            key = "host"
                    assert(key != None)
                    dict2[key] = node1
                node2 = globals()[class2](**dict2)
                self.add_node(node2)
            self.Connections.append([node1, node2])
        # Handle retrieval of isolated nodes
        session.close()
        session = Session()
        for c in MappedClasses:
            for element in eval("session.query(" + c + ").all()"):
                dictionary = element.__dict__
                del dictionary['_sa_instance_state']
                dictionary['gui'] = self
                if not self.find_node_id(element.ident):
                    node = globals()[c](**dictionary)
                    self.add_node(node)
        session.close()

    def add_node(self, node):
        self.add_node_bare(node)
        node.put_on_layout(self.layout)

    def add_node_bare(self, node):
        self.lock.acquire()
        self.NodeList.append(node)
        self.lock.release()

    def get_foreground_gc(self):
        self.style = self.layout.get_style()
        self.GC = self.style.fg_gc[gtk.STATE_NORMAL] 

    def draw_circle(self, x, y, radius):
        self.layout.bin_window.draw_arc(self.GC, True, x, y, radius, radius,
                                        0, 360*64)

    def draw_edge(self, x1, y1, x2, y2):
        # FIXME: a bezier curve would definitely look better
        self.layout.bin_window.draw_line(self.GC, x1, y1, x2, y2) 

    def draw_grid(self, distance, width, height):
        # Plot coordinates at distance until width and/or height are reached
        for x in range(distance, width, distance):
            for y in range(distance, height, distance):
                self.draw_circle(x, y, 2)

    def draw_connections(self):
        for conn in self.Connections:
            self.draw_edge(conn[0].x, conn[0].y, conn[1].x, conn[1].y)

    def search_for_node(self, field, content):
        # FIXME: multiple objects can be returned?
        for node in self.NodeList:
            if field in node.__dict__.keys():
                if str(node.__dict__[field]) == str(content):
                    return node
        return None

    def search_for_node_with_class(self, classname, field, content):
        for node in self.NodeList:
            if field in node.__dict__.keys():
                if str(node.__dict__[field]) == str(content):
                    if node.__class__.__name__ == classname:
                        return node
        return None 

    def connection_exists(self, node1, node2):
        try:
            next(x for x in self.Connections if x == [node1, node2])
            next(x for x in self.Connections if x == [node2, node1])
        except StopIteration:
            pass
        else:
            return True
        return False

    def get_new_node(self, classname, field, content, x, y):
        # Set default values for new node
        # FIXME: automatically compute position for new object?
        x += 40
        y += 40
        args_dict = {'name': 'New', 'x': x, 'y': y, 'gui': self}
        # Handle unique identifier
        if field != 'ident':
            args_dict['ident'] = str(self.counter.get())
        # Set required field
        if field != None:
            args_dict[field] = content
        # Get new instance of requested class
        newnode = globals()[classname](**args_dict)
        assert(newnode != None)
        self.add_node(newnode)
        return newnode

    def new_node_request(self, widget, event, classname):
        self.get_new_node(classname, "ident", self.counter.get(), 30, 30)

    def has_priority_over(self, class1, class2):
        classes_prio = ["IP_address", "Host", "WebServer", "DNS_server"]
        assert(class1 in classes_prio and class2 in classes_prio)
        if classes_prio.index(class1) == classes_prio.index(class2):
            return True
        if classes_prio.index(class1) < classes_prio.index(class2):
            return True
        else:
            return False

    def get_connection_with_priority(self, node1, node2):
        if self.has_priority_over(node1.__class__.__name__,
                                  node2.__class__.__name__):
            return (node1, node2)
        else:
            return (node2, node1)

    def connect(self, node1, node2):
        if node1 is node2:
            return
        assert(node1 != None and node2 != None)
        # If nodes are not in the NodeList, just add them and
        # be confident that they will put on their layout later
        if node1 not in self.NodeList:
            self.add_node_bare(node1)
        if node2 not in self.NodeList:
            self.add_node_bare(node2)
        assert(node1 in self.NodeList and node2 in self.NodeList)
        # Check if the connection already exists before creating a new one
        if not self.connection_exists(node1, node2):
            assert(node1.ident != node2.ident)
            (node1, node2) = self.get_connection_with_priority(node1, node2)
            print node1.__class__.__name__, node2.__class__.__name__
            self.Connections_obj.append(Connection(node1.ident, node2.ident,
                                                   node1.__class__.__name__,
                                                   node2.__class__.__name__ ))
            self.Connections.append([node1, node2])

#-------------------------------------------------------------------------------

def refresh_drawing_area (da):
    da.queue_draw()
    return True

if __name__ == "__main__":
    counter = Counter()
    app = Locator(counter)
    # Grab a reference on the DrawingArea
    da = app.get_da()

    NodeList = [
        Smiley(ident=counter.get(), name='Very Happy', x=50 , y=50, gui=app),
        IP_address(ident=counter.get(), x=50, y=200, ip="192.168.0.1", gui=app),
        Person(ident=counter.get(), x=300, y=400, surname="9", gui=app),
        ]
    NodeList.append( DNS_server(ident=counter.get(), name='DNSS', ipaddr=None, x=150, y=100, gui=app) )
    NodeList.append( Host(ident=counter.get(), name='HOST', ipaddr=None, x=200, y=200, gui=app) )
    NodeList.append( WebServer(ident=counter.get(), name='WEBSRV', host=None, x=250, y=200, gui=app) )

    for node in NodeList :
        app.add_node(node)

    # Gtk will forget about refreshing the DrawingArea while dragging and
    # dropping. Remind him every 70 milliseconds.
    gtk.timeout_add(70, refresh_drawing_area, da)

    gtk.main()

# vim: set et sts=4 sw=4:
