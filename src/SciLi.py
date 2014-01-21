#!/usr/bin/env python

import os

from gi.repository import Gtk
from ui import SciLiWindow

class SciLiApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = SciLiWindow(self)
        win.show_all()

if __name__ == "__main__":

    app = SciLiApp()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
