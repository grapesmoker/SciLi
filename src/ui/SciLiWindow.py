from gi.repository import Gtk

class SciLiWindow(Gtk.ApplicationWindow):

    def __init__(self, app):

        Gtk.Window.__init__(self, title="SciLi", application=app)

        main_grid = Gtk.Grid()

        left_pane = Gtk.Grid()
        right_pane = Gtk.Grid()
        center_pane = Gtk.Grid()

        toolbar = Gtk.Toolbar()
        statusbar = Gtk.StatusBar()

        main_grid.attach(toolbar, 0, 0, 3, 1)
        main_grid.attach(left_pane, 1, 0, 1, 1)
        main_grid.attach(center_pane, 1, 1, 1, 1)
        main_grid.attach(right_pane, 1, 2, 1, 1)
        main_grid.attach(status_bar, 2, 1, 3, 1)

        self.add(grid)

    
