#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# A resource locator which draws connected resources in a graph
#
import pygtk
pygtk.require('2.0')
import gtk

from Counter import *
from Smiley import *
from Host import *
from Person import *
from IP_address import *
from WebServer import *
from DNS_server import *

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

        self.counter = counter

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

    def add_node(self, node):
        self.NodeList.append(node)
        node.put_on_layout(self.layout)

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
        # FIXME: multiple objects can be returned? Not if ident is unique
        for node in self.NodeList:
            if field in node.__dict__.keys():
                if str(node.__dict__[field]) == str(content):
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

    def get_new_node(self, classname, field, content):
        command = classname + "("
        if field != "ident":
            command = command + "ident=" + str(self.counter.get()) + ", "
        prova = command + str(field) + "='" + str(content) + "', name='New', x=100, y=100, gui=self)"
        print prova
        newnode = eval(prova)
        assert(newnode != None)
        self.add_node(newnode)
        return newnode

    def new_node_request(self, widget, event, classname):
        self.get_new_node(classname, "ident", self.counter.get())    

    def connect(self, node1, node2):
        if node1 is node2:
            return
        assert(node1 != None and node2 != None)
        assert(node1 in self.NodeList and node2 in self.NodeList)
        # Check if the connection already exists before creating a new one
        if not self.connection_exists(node1, node2):
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
        Smiley(ident=counter.get(), name='very happy', Type='Data', x=50 , y=50, gui=app),
        DNS_server(ident=counter.get(), name='happy', Type='App', x=150, y=100, gui=app),
        WebServer(ident=counter.get(), name='server', Type='Data', x=250, y=200, gui=app),
        IP_address(ident=counter.get(), Type='Data', x=50, y=200, ip="192.168.0.1", gui=app),
        Person(ident=counter.get(), x=300, y=400, surname="9", gui=app),
        ]
    for node in NodeList :
        app.add_node(node)

    # Gtk will forget about refreshing the DrawingArea while dragging and
    # dropping. Remind him every 70 milliseconds.
    gtk.timeout_add(70, refresh_drawing_area, da)

    gtk.main()

# vim: set et sts=4 sw=4:
