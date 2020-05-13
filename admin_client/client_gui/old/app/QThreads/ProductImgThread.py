from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal,QObject
from PyQt5.QtWidgets import QFileDialog,QWidget
from PyQt5.QtGui import QIcon

class getProductImages(QObject):
    w=None
    fname=pyqtSignal(QObject)
    filename=None
    qthreaded=None
    def openFileNameDialog(self):
        options=QFileDialog.Option()
        options |= QFileDialog.DontUseNativeDialog
        filename,_= QFileDialog.getOpenFileName(self.w,"Product Image","","PNG (*.png);;JPEG (*.jpg);;JPEG (*.jpeg)",options=options)
        if filename:
            self.filename=filename
            self.fname.emit(self) 
