from PyQt5 import uic
from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal,QObject,QThreadPool,QModelIndex

from PyQt5.QtWidgets import QDialog,QComboBox,QWidget,QListWidgetItem,QListWidget,QStackedWidget
import ast,json,sys,os,requests
from .widgets.UpdateSelector import UpdateSelector 
from PyQt5.QtGui import QStandardItemModel

from .widgets.address.AddressStack import AddressStack

class DeleteDialog(QDialog):
    auth:tuple=None
    address:str=None
    w:QWidget=None
    dialog:QDialog=None
    def __init__(self,parent:QWidget,address:str,auth:tuple):
        super(DeleteDialog,self).__init__()

        self.auth=auth
        self.address=address
        self.w=parent
        self.dialog=QDialog(parent)
        uic.loadUi("app/DeleteDialog/forms/DeleteDialog.ui",self.dialog)

        self.qtp=QThreadPool.globalInstance()
        updaterSelector=UpdateSelector(self.w,self.dialog.selector)
        updaterSelector.signals.ready.connect(self.selector_ud)
        self.qtp.start(updaterSelector)        
        self.dialog.selector.activated.connect(self.stack_changer)
        
        #widget
        self.address=AddressStack(self.w,self.dialog.address,self.dialog,self.auth,self.address)
        self.address.done_del.connect(self.progress_statement) 


        self.dialog.show() 

    def progress_statement(self):
        print("Done Deleting Object")
        self.w.sb.showMessage("Done Deleting Object!",10)

    def stack_changer(self,index:QModelIndex):
        self.dialog.views.setCurrentIndex(index.row())
        print(self.dialog.views.currentWidget().objectName())
        self.address.isVisible(self.dialog.views.currentWidget().objectName())
        #QListWidget.

    def selector_ud(self,model):
        for i in model:
            self.dialog.selector.addItem(QListWidgetItem(i))


