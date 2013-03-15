# -*- coding: utf-8 -*-
#
# A most important resource in a network
#
from Node import *

class Smiley(Node):

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

# vim: set et sts=4 sw=4:
