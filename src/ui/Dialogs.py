import pymongo

from gi.repository import Gtk

def parse_metadata(filename):

    pass

class NewLibraryDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "New Library", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        box = self.get_content_area()

        label = Gtk.Label("Enter library name:")
        lib_name = Gtk.Entry()

        self.entry = lib_name

        box.add(label)
        box.add(lib_name)

        self.show_all()
        

class NewRecordDialog(Gtk.Dialog):

    def __init__(self, parent):
        
        Gtk.Dialog.__init__(self, "New Record", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        box = self.get_content_area()

        grid = Gtk.Grid()

        button = Gtk.Button("Choose file")
        button.connect("clicked", self.on_file_clicked)
        
        label_filename = Gtk.Label("Filename: ")
        label_authors = Gtk.Label("Authors (Last, First; one per line): ")
        label_affiliations = Gtk.Label("Affiliations (one per line): ")
        label_journal = Gtk.Label("Journal: ")
        label_pub_date = Gtk.Label("Publication Date: ")
        label_volume = Gtk.Label("Volume: ")
        label_issue = Gtk.Label("Issue: ")
        label_pages = Gtk.Label("Pages: ")
        label_abstract = Gtk.Label("Abstract: ")
        label_keywords = Gtk.Label("Keywords (comma separated): ")
        label_url = Gtk.Label("URL: ")
        
        self.entry_filename = Gtk.Entry()
        self.text_authors = Gtk.TextView()
        self.text_buf_authors = self.text_authors.get_buffer()

        self.text_affiliations = Gtk.TextView()
        self.text_buf_affiliations = self.text_affiliations.get_buffer()

        self.entry_journal = Gtk.Entry()
        self.entry_pub_date = Gtk.Entry()
        self.entry_volume = Gtk.Entry()
        self.entry_issue = Gtk.Entry()
        self.entry_pages = Gtk.Entry()

        self.text_abstract = Gtk.TextView()
        self.text_buf_abstract = self.text_abstract.get_buffer()

        self.text_keywords = Gtk.TextView()
        self.text_buf_keywords = self.text_keywords.get_buffer()

        self.entry_url = Gtk.Entry()

        grid.attach(label_filename, 0, 0, 1, 1)
        grid.attach(self.entry_filename, 1, 0, 1, 1)
        grid.attach(button, 2, 0, 1, 1)

        grid.attach(label_authors, 0, 1, 1, 1)
        grid.attach(self.text_authors, 1, 1, 2, 1)
        
        grid.attach(label_affiliations, 0, 2, 1, 1)
        grid.attach(self.text_affiliations, 1, 2, 2, 1)
        
        grid.attach(label_journal, 0, 3, 1, 1)
        grid.attach(self.entry_journal, 1, 3, 1, 1)
        
        grid.attach(label_pub_date, 0, 4, 1, 1)
        grid.attach(self.entry_pub_date, 1, 4, 1, 1)
        
        grid.attach(label_volume, 0, 5, 1, 1)
        grid.attach(self.entry_volume, 1, 5, 1, 1)
        
        grid.attach(label_issue, 0, 6, 1, 1)
        grid.attach(self.entry_issue, 1, 6, 1, 1)
        
        grid.attach(label_pages, 0, 7, 1, 1)
        grid.attach(self.entry_pages, 1, 7, 1, 1)
        
        grid.attach(label_abstract, 0, 8, 1, 1)
        grid.attach(self.text_abstract, 1, 8, 2, 1)

        grid.attach(label_keywords, 0, 9, 1, 1)
        grid.attach(self.text_keywords, 1, 9, 2, 1)
        
        grid.attach(label_url, 0, 10, 1, 1)
        grid.attach(self.entry_url, 1, 10, 1, 1)
        
        box.add(grid)
        self.show_all()

    def on_file_clicked(self, widget):

        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter_pdf = Gtk.FileFilter()
        filter_pdf.set_name("PDF files")
        filter_pdf.add_mime_type("application/pdf")
        dialog.add_filter(filter_pdf)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()

        filename = self.entry_filename.get_text()
        if response == Gtk.ResponseType.OK:
            if os.path.exists(filename):
                self.entry_filename.set_text(filename)
                parse_metadata(filename)

        dialog.destroy()



    
