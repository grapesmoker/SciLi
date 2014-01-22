import sys
import pymongo
import os

from pymongo import MongoClient
from gi.repository import Gtk

from ui.Dialogs import *

class SciLiWindow(Gtk.ApplicationWindow):

    def __init__(self, app):

        Gtk.Window.__init__(self, title="SciLi", application=app)

        self.set_default_size(640, 480)

        self.main_grid = Gtk.Grid()

        self.left_pane = Gtk.Grid()
        self.right_pane = Gtk.Grid()
        self.center_pane = Gtk.Grid()

        self.toolbar = Gtk.Toolbar()
        #self.toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR);
        self.toolbar.set_hexpand(True)
        self.toolbar.show()

        self.statusbar = Gtk.Statusbar()

        self.main_grid.attach(self.toolbar, 0, 0, 3, 1)
        self.main_grid.attach(self.left_pane, 0, 1, 1, 1)
        self.main_grid.attach(self.center_pane, 1, 1, 1, 1)
        self.main_grid.attach(self.right_pane, 2, 1, 1, 1)
        self.main_grid.attach(self.statusbar, 0, 2, 3, 1)

        self.add(self.main_grid)

        self.create_toolbar()
        self.setup_db()
        self.setup_left_pane()

        self.library_action_group = Gtk.ActionGroup("library")
        self.record_action_group = Gtk.ActionGroup("record")

        self.current_lib = None

    def setup_db(self):

        self.client = MongoClient()
        self.db = self.client.scili_db
        self.libraries = self.db.libraries
        self.records = self.db.records
        self.collections = self.db.collections
        
    def setup_left_pane(self):

        self.left_store = Gtk.TreeStore(str)
        #top_level_categories = ['Libraries', 'Sources', 'Collections']

        sources = ['ArXiv', 'PUBMed', 'Your Mom']

        all_libraries = self.libraries.find()
        piter = self.left_store.append(None, ['Libraries'])
        for lib in all_libraries:
            self.left_store.append(piter, [lib['name']])

        piter = self.left_store.append(None, ['Sources'])
        for s in sources:
            self.left_store.append(piter, [s])

        all_collections = self.collections.find()
        piter = self.left_store.append(None, ['Collections'])
        for coll in all_collections:
            self.left_store.append(piter, [coll['name']])

        self.left_view = Gtk.TreeView()
        self.left_view.set_model(self.left_store)
        renderer_txt = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Actions", renderer_txt, text=0)
        self.left_view.append_column(column)
        self.left_view.connect("row-activated", self.on_left_row_activated)

        select = self.left_view.get_selection()
        select.connect("changed", self.on_selection_changed)

        self.left_pane.add(self.left_view)

    def on_selection_changed(self, selection):

        model, treeiter = selection.get_selected()
        if treeiter is not None:
            pass
            #print model[treeiter][0]

        # code to display stuff in central pane goes here

    def on_left_row_activated(self, widget, path, column):

        print path

        tree_iter = self.left_store.get_iter(path)

        val = self.left_store.get_value(tree_iter, 0)
        print val
        if val == 'Libraries':
            citer = self.left_store.get_iter(path)
            piter = self.left_store.iter_parent(citer)
            print self.left_store[piter][0]

    def create_toolbar(self):

        button_new = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        button_open = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OPEN)
        button_add_record = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)

        sep = Gtk.Separator()

        self.toolbar.insert(button_new, 0)
        self.toolbar.insert(button_open, 1)
        self.toolbar.insert(button_add_record, 2)

        action_new = Gtk.Action("NewLibrary", "_New", "Create a new library", Gtk.STOCK_NEW)
        action_new.connect("activate", self.create_new_library)

        button_new.connect("clicked", self.create_new_library)
        button_add_record.connect("clicked", self.add_record)

    def create_new_library(self, obj_clicked):

        dialog = NewLibraryDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            lib_name = dialog.entry.get_text()
            existing_lib = self.libraries.find_one({'name': lib_name})
            if existing_lib is not None:
                message_dialog = Gtk.MessageDialog(parent=self,
                                                   flags=Gtk.DialogFlags.MODAL,
                                                   type=Gtk.MessageType.WARNING,
                                                   buttons=Gtk.ButtonsType.OK,
                                                   message_format="A library named {0} already exists!".format(lib_name))
            else:
                self.libraries.insert({'name': lib_name})
                message_dialog = Gtk.MessageDialog(parent=self,
                                                   flags=Gtk.DialogFlags.MODAL,
                                                   type=Gtk.MessageType.INFO,
                                                   buttons=Gtk.ButtonsType.OK,
                                                   message_format="Library {0} created!".format(lib_name))

            message_dialog.connect("response", lambda widget, response: widget.destroy())
            message_dialog.show()

        dialog.destroy()

    def add_record(self, widget):
        
        dialog = NewRecordDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            record = {}

            record['filename'] = dialog.entry_filename.get_text()
            record['journal'] = dialog.entry_journal.get_text()
            record['pub_date'] = dialog.entry_pub_date.get_text()
            record['volume'] = dialog.entry_volume.get_text()
            record['issue'] = dialog.entry_issue.get_text()
            record['pages'] = dialog.entry_pages.get_text()
            record['url'] = dialog.entry_url.get_text()

            authors_text = dialog.text_buf_authors.get_text(dialog.text_buf_authors.get_start_iter(),
                                                            dialog.text_buf_authors.get_end_iter(),
                                                            False).split('\n')

            print authors_text
            authors = []
            for auth in authors_text:
                if auth.find(',') != -1:
                    first_name, last_name = auth.split(',')
                else:
                    first_name = ''
                    last_name = auth
                    author = {'first_name': first_name, 'last_name': last_name}
                    authors.append(author)

            record['authors'] = authors
            record['keywords'] = dialog.text_buf_keywords.get_text(dialog.text_buf_keywords.get_start_iter(),
                                                                   dialog.text_buf_keywords.get_end_iter(),
                                                                   False).split(',')
            record['abstract'] = dialog.text_buf_abstract.get_text(dialog.text_buf_abstract.get_start_iter(),
                                                                   dialog.text_buf_abstract.get_end_iter(),
                                                                   False)
            record['affiliations'] = dialog.text_buf_affiliations.get_text(dialog.text_buf_affiliations.get_start_iter(),
                                                                           dialog.text_buf_affiliations.get_end_iter(),
                                                                           False).split('\n')

            print record
                

        dialog.destroy()
