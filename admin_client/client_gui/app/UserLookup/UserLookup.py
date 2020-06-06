from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json,ast,requests

class UserLookup(QDialog):
    def __init__(self,auth:dict,parent:QWidget):
        super(UserLookup,self).__init__()
        self.auth=auth
        self.parent=parent
        self.dialog=QDialog()
        uic.loadUi("app/UserLookup/forms/UserLookup.ui",self.dialog)



        self.dialog.exec_()
