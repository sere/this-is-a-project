# -*- coding: utf-8 -*-
#
# Base class for a resource (node) in a graph representation
#
import pygtk
pygtk.require('2.0')
import gtk
import subprocess

# FIXME: This is a base class and must be refined to contain just the drawing
#	 methods and other methods that will be common to all "physical" classes

# Drag'n'Drop
TARGET_TYPE_NDDE = 80
fromNode = [ ( "node_move", 0, TARGET_TYPE_NDDE ),]

class Node:

    dataPanel = None

    tiny_pixbuf = None
    find_neighbors_script = None
    features = ["x", "y", "name"]

    def __init__(self,name=None,Type='Data',x=50, y=50, ident=None, gui=None):
        self.Type = Type
        self.x = x
        self.y = y
        self.ident = ident
        assert(ident != None)
	self.name = "%s%s" % (name or Type, str(self.ident))
        self.gui = gui
	assert(self.gui != None)

        # image
        self.Image_EventBox = gtk.EventBox()
        self.Image_EventBox.set_border_width(0)

        self.Image = gtk.Image()
        self.Image.set_from_pixbuf(self.tiny_pixbuf)
        self.Image_EventBox.add(self.Image)

        self.Image.show()
        self.Image_EventBox.show()

        # Label
        self.Label_EventBox = gtk.EventBox()
        self.Label_EventBox.set_border_width(0)

        self.Label = gtk.Label(self.__repr__())
        self.Label.set_justify(gtk.JUSTIFY_CENTER)
        self.Label.set_size_request(width=66, height=-1)
        self.Label.set_line_wrap(True)
        self.Label_EventBox.add(self.Label)

	# Data Panel
	self.dataPanel = gtk.EventBox()
	self.dataPanel.set_border_width(0)

	self.dataPanel_label = gtk.Label("Dati")
	self.dataPanel_label.set_justify(gtk.JUSTIFY_CENTER)
	self.dataPanel_label.set_size_request(width=100, height=-1)
	self.dataPanel_label.set_line_wrap(True)
	self.dataPanel.add(self.dataPanel_label)

        # Drag'n'drop
        self.Image_EventBox.connect("drag_begin", self.begin_Callback)
        self.Image_EventBox.connect("drag_data_get", self.send_Callback)
        self.Image_EventBox.drag_source_set(gtk.gdk.BUTTON1_MASK,fromNode,
                               gtk.gdk.ACTION_COPY)
        self.Image_EventBox.connect("button-release-event", self.node_clicked)
        self.Image_EventBox.set_events(gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK )
        self.Image_EventBox.connect("button-press-event", self.modify_features)
	self.Image_EventBox.connect("enter-notify-event", self.show_features)
	self.Image_EventBox.connect("leave-notify-event", self.hide_features)

        self.Label.show()
        self.Label_EventBox.show()

    def begin_Callback(self, widget, context):
        widget.drag_source_set_icon_pixbuf(self.tiny_pixbuf)

    def send_Callback(self, widget, context, selection, targetType, time):
        if targetType == TARGET_TYPE_NDDE:
            selection.set(selection.target, 8, str(id(self)))

    def put_on_layout(self,layout):
        layout.put(self.Image_EventBox, self.x, self.y)
        layout.put(self.Label_EventBox, self.x-15, self.y+28)
	layout.put(self.dataPanel, self.x+30, self.y-30)

    def move_on_layout(self, da, layout, x, y):
        self.x = int(x + layout.get_hadjustment().value)
        self.y = int(y + layout.get_vadjustment().value)
        layout.move(self.Image_EventBox, self.x   , self.y)
        layout.move(self.Label_EventBox, self.x-15, self.y+28)
	layout.move(self.dataPanel, self.x+30, self.y-30)

    def show_features(self, widget, event):
	# Show features of node around object
	newlabel = ""
	for name in self.features:
		newlabel = newlabel + " " + name + ":" + str(eval('self.' + name))
	self.dataPanel_label.set_label(newlabel)
	self.dataPanel_label.show()
	self.dataPanel.show()

    def hide_features(self, widget, event):
	# Hide features of node
	self.dataPanel_label.hide()
	self.dataPanel.hide()

    def get_changes(self, widget, event, window, textboxes):
        for elem in textboxes:
            label = elem[0]
            text = elem[1]
            setattr(self, str(label.get_text()), str(text.get_text()))
        # Refresh representation
        self.Label.set_text(self.__repr__())
        # Drop everything now; window hide will drop all textboxes
        window.hide_all()
        pass

    def drop_changes(self, widget, textboxes):
        del textboxes[:]  

    def modify_features(self, widget, event):
        # Modify only on double click
        if event.type == gtk.gdk._2BUTTON_PRESS:
            # Create temporary window
            textboxes = []
            window = gtk.Window()
            window.set_title("Modify " + self.name)
            vbox = gtk.VBox(False, 0)
            # Get all features and modify them
            for feature in self.features:
                hbox = gtk.HBox(False, 0)
                label = gtk.Label(str=feature)
                hbox.pack_start(label, False, True, 0)
                text = gtk.Entry()
                text.set_text(str(eval("self." + feature)))
                hbox.pack_start(text, False, True, 0)
                textboxes.append([label, text])
                vbox.pack_start(hbox, False, True, 0)
            button = gtk.Button(label="Change")
            button.connect("button-press-event", self.get_changes, window, textboxes)
            vbox.pack_start(button, False, True, 0)
            window.add(vbox)
            window.connect("hide", self.drop_changes, textboxes)
            window.show_all()

    # It may be useful to redefine this in derived classes
    def node_clicked(self, widget, event):
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

    def runProcess(self, exe):
        return subprocess.check_output(exe)

    # This is most likely to be redefined in derived classes, as different
    # categories may want to find neighbors with different criteria
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

    def __repr__(self):
        return str(self.ident)

# vim: set et sts=4 sw=4:
