'''
Created on Dec 11, 2012

@author: jerry
'''

import re

from PyQt4 import QtGui, QtCore
from ui.mainwindow import Ui_MainWindow
from ui.new_record import Ui_Dialog
from Interface.Dialogs import AddRecordDialog
from pymongo import MongoClient

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.library_model = QtGui.QStandardItemModel(0, 3, None)
        self.library_model.setHorizontalHeaderLabels(['Name', 'Author', 'Type'])
        self.library = None
        
        self.ui.tableView.setModel(self.library_model)
        
        lib_menu = QtGui.QMenu()
        self.actionNew_Library = lib_menu.addAction('New Library')
        self.actionOpen_Library = lib_menu.addAction('Open Library')
        self.actionAdd_Record = lib_menu.addAction('Add Record')
        
        self.ui.actionLibrary.setMenu(lib_menu)
        
        self.db_connection = MongoClient('localhost', 27017)
        self.scili_db = self.db_connection.scili_db
        self.libraries = self.scili_db.libraries
        self.documents = self.scili_db.documents
        self.journals = self.scili_db.journals
        
        self.actionNew_Library.triggered.connect(self.new_library)
        self.actionAdd_Record.triggered.connect(self.add_record)
        self.actionOpen_Library.triggered.connect(self.open_library)
        
    def new_library(self):

        new_library_name, accepted = QtGui.QInputDialog.getText(self, 'New library', 'Enter library name')
        new_library_name = unicode(new_library_name)

        if accepted:
            num_libs = self.libraries.find({'name': new_library_name.encode()}).count()
            if num_libs > 0:
                QtGui.QMessageBox.information(self, 
                                              'Library exists!', 
                                              'A library with that name already exists!')
            else:
                self.library = self.libraries.insert({'name': new_library_name})
                
    def open_library(self):
        
        available_libraries = [library for library in self.libraries.find()]
        lib_names = [lib['name'] for lib in available_libraries]
        lib_combo_box = QtGui.QInputDialog()
        #lib_combo_box.setComboBoxEditable(False)
        lib_to_open, accepted = lib_combo_box.getItem(self, 
                                                      'Open library',
                                                      'Select library to open', 
                                                      lib_names, 
                                                      editable=False)
        lib_to_open = unicode(lib_to_open)
        if accepted:
            self.library = self.libraries.find_one({'name': lib_to_open.encode()})
        
        # TODO: some stuff goes here to load all the records into the table
        
    def add_record(self):
        
        if self.library is None:
            QtGui.QMessageBox.warning(self,
                                      'No active library!',
                                      'You have no library open. Either open an \
                                      existing library or create a new one.')
        else:
            dialog_window = AddRecordDialog(parent=self)
            dialog_window.exec_()
            if dialog_window.result() == QtGui.QDialog.Accepted:
                authors_text = dialog_window.ui.txtAuthors.document().toPlainText().split('\n')
                authors = []
                for author_name in authors_text:
                    print author_name
                    author_first, author_last = author_name.split(',')
                    authors.append({'first_name': author_first,
                                    'last_name': author_last})
                new_record = {'filename': dialog_window.ui.txtFilename.text(),
                              'title': dialog_window.ui.txtTitle.text(),
                              'authors': authors,
                              'affiliation': dialog_window.ui.cmbAffiliation.currentText(),
                              'journal': dialog_window.ui.cmbJournal.currentText(),
                              'pub_date': dialog_window.ui.txtPubDate.text(),
                              'volume': dialog_window.ui.txtVolume.text(),
                              'issue': dialog_window.ui.txtIssue.text(),
                              'pages': dialog_window.ui.txtPages.text(),
                              'abstract': dialog_window.ui.txtAbstract.document().toPlainText(),
                              'editor': dialog_window.ui.txtEditor.text(),
                              'publisher': dialog_window.ui.cmbPublisher.currentText(),
                              'tags': dialog_window.ui.txtKeywords.document().toPlainText(),
                              'library': self.library}
                print new_record
                self.documents.insert(new_record)
                
            else:
                print "ffoo"
        
        
    def test(self):
        self.filename = QtGui.QFileDialog.getOpenFileName()
        print self.filename
        
        