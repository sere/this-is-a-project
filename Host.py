# -*- coding: utf-8 -*-
#
# Representation of a host
#
import os, threading
from Node import *
from IP_address import *

class Host(Node):

    # ipaddr is an istance of the class IP_address, 
    # while ip represents the "real" ip of the host
    read_features = ["ip", "netmask", "network", "interface"]
    features = ["ip", "netmask", "interface"]

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
        "-..XXXXXXXXXXXXXXXXXXXX..-",
        "-..XXXXXXXXXXXXXXXXXXXX..-",
        "-..XXXXXXXXXXXXXXXXXXXX..-",
        "-..XXXXXXXXXXXXXXXXXXXX..-",
        "-..XXXXXXXXXXXXXXXXXXXX..-",
        "-..XXXXXXXXXXXXXXXXXXXX..-",
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


    def __init__(self, name=None, ipaddr=None, netmask="24", interface="wlan0", Type='Data', x=50, y=50, ident=None, gui=None):
        if ipaddr == None:
            ipaddr = gui.get_new_node("IP_address", None, None)
        assert(ipaddr != None)
        self.ipaddr = ipaddr 
        self.ip = self.ipaddr.getIp()
        self.network = self.get_network(self.ip)
        self.netmask = netmask
        self.interface = interface
	Node.__init__(self, name, Type, x, y, ident, gui)
	self.find_neighbors_script = "./script_ip.sh"
        self.refresh_data_script = "./refresh_data.sh"
        self.find_up_script = "./get_up.sh"

    def get_network(self, ip):
        return ".".join(ip.split(".")[:-1]) + ".0"

    def get_changes(self, widget, event, window, textboxes):
        for elem in textboxes:
            label = elem[0]
            text = elem[1]
            # If we are modifying the ip, be sure to refresh also the
            # data in the IP_address structure
            if label == 'ip':
                self.ipaddr.setIp(text)
            setattr(self, str(label.get_text()), str(text.get_text()))
        # Refresh representation
        self.Label.set_text(self.__repr__())
        # Drop everything now; window hide will drop all textboxes
        window.hide_all()

    def node_clicked(self, widget, event):
        # If right-click
        if event.button == 3:
            newmenu = gtk.Menu()
            newitem = gtk.MenuItem('Find neighbors (ip)')
            newmenu.append(newitem)
            newitem.connect("button-press-event", self.find_neighbors)
            newitem1 = gtk.MenuItem('Refresh data')
            newmenu.append(newitem1)
            newitem1.connect("button-press-event", self.refresh_data)
            newitem2 = gtk.MenuItem('Find up hosts')
            newmenu.append(newitem2)
            newitem2.connect("button-press-event", self.find_up)
            newmenu.show_all()
            newmenu.popup(None, None, None, event.button, event.time)

    # Refresh host information with the current machine's
    def refresh_data(self, widget, event):
        out = self.runProcess([self.refresh_data_script, self.interface])
        self.ip = str(out).strip().split()[0]
        self.ipaddr.setIp(str(out).strip().split()[0])
        self.network = self.get_network(self.ip)
        self.netmask = str(out).strip().split()[1]

    def find_connect_node(self, newid):
        # Search for IP_address instance and eventually create a new one
        ipaddr = self.gui.search_for_node_with_class("IP_address", "ip", newid)
        if ipaddr == None:
            ipaddr = self.gui.get_new_node("IP_address", "ip", newid)
        # Create new host
        classname = self.__class__.__name__
        neigh = self.gui.search_for_node_with_class(classname, "ipaddr", ipaddr)
        if neigh == None:
            neigh = self.gui.get_new_node(classname, "ipaddr", ipaddr)
        self.gui.connect(self, neigh)

    # Find up hosts
    def find_up(self, widget, event):
        if os.geteuid() != 0:
            print "This functionality needs root privileges"
            return
        def my_thread(obj):
            # FIXME: locking!
            print "Exploring " + self.network + "/" + self.netmask + "..."
            out = obj.runProcess([self.find_up_script, self.network, self.netmask])
            print "... done."
            for newip in str(out).strip().split():
                print "Found " + newip
                obj.find_connect_node(newip)
        threading.Thread(target=my_thread, args=(self,)).start()

    # Search by ip
    def find_neighbors(self, widget, event):
        out = self.runProcess([self.find_neighbors_script])
        for newid in str(out).strip().split():
            self.find_connect_node(newid)

# vim: set et sts=4 sw=4:
