from PyQt5.QtCore import QObject,QThread,QThreadPool,pyqtSignal,pyqtSlot,QCoreApplication
from PyQt5.QtWidgets import QWidget

class MenuBar:
    def __init__(self,mainWindow:QWidget):
        self.mainWindow=mainWindow
        self.mainWindow.actionLogout.triggered.connect(self.logOut) 
        if self.mainWindow.application.currentIndex() < 1:
            self.mainWindow.actionLogout.setEnabled(False)

    def logOut(self):
        self.mainWindow.application.setCurrentIndex(0)
        self.mainWindow.actionLogout.setEnabled(False)

    def loggedIn(self,index):
        if index > 0:
            self.mainWindow.actionLogout.setEnabled(True)
