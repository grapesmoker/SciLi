#!/usr/bin/env python

import os
import sys
import pymongo

from gi.repository import Gtk
from ui.SciLiWindow import SciLiWindow

class SciLiApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = SciLiWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

if __name__ == "__main__":

    app = SciLiApp()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
