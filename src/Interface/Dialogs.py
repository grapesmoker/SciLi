from ui.new_record import Ui_Dialog
from PyQt4 import QtGui, QtCore

class AddRecordDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.btnSelectFile.clicked.connect(self.get_record_filename)
        
    def get_record_filename(self):
        self.filename = QtGui.QFileDialog.getOpenFileName()
        print self.filename
        self.ui.txtFilename.setText(self.filename[0])
        
class NewLibraryDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        
        QtGui.QDialog.__init__(self, parent)
        