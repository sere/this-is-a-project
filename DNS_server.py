# -*- coding: utf-8 -*-
#
# Representation of a host
#
from Node import *

class DNS_server(Node):

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

    
# vim: set et sts=4 sw=4:
