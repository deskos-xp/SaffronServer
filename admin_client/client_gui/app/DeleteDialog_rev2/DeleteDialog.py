from PyQt5.QtCore import QObject,QRunnable,pyqtSignal,pyqtSignal,QThreadPool,pyqtSlot,QModelIndex
from PyQt5.QtWidgets import QWidget,QDialog,QListView,QStackedWidget,QComboBox

import os,sys,json,ast
from PyQt5 import uic
from .DeleteDialogModel import DeleteDialogModel
from .workers.GetComboData import GetComboData

class DeleteDialog(QDialog):
    def __init__(self,auth:dict):
        super(DeleteDialog,self).__init__()
        self.dialog=QDialog()
        self.auth=auth
        uic.loadUi("app/DeleteDialog_rev2/forms/DeleteDialog.ui",self.dialog)        
        self.items=["Address","Brand","Vendor","Manufacturer","Department","Product"]
        #QStackedWidget.findChild
        self.model=DeleteDialogModel(items=self.items)
        self.model.layoutChanged.emit()
        
        self.dialog.selector.clicked.connect(self.updateViews)
        self.dialog.selector.setModel(self.model)

        #self.modelsList=list()
        #self.models=dict()
        self.workers=dict()

        for i in self.items:
            uic.loadUi("app/DeleteDialog_rev2/forms/DeleteDialogItemView.ui",getattr(self.dialog,i.lower()))
            getattr(self.dialog,i.lower()).setObjectName(i.lower())
            getattr(self.dialog,i.lower()).entityName.setText(i[0].upper()+i[1:])
            getattr(self.dialog,i.lower()).confirm.rejected.connect(self.dialog.reject)
            
            #QComboBox.currentIndexChanged()
            getattr(self.dialog,i.lower()).items.activated.connect(lambda x: self.updateViewer(x,i.lower()))

            self.workers[i.lower()]=GetComboData(self.auth,i.lower())
            self.workers[i.lower()].signals.hasError.connect(lambda x:print(x))
            self.workers[i.lower()].signals.hasItems.connect(self.updateCombo)

            QThreadPool.globalInstance().start(self.workers[i.lower()])
            #update from worker


        self.dialog.exec_()

    def updateViewer(self,index,name):
        print(self.sender().currentText())
        #self.models[name]


    @pyqtSlot(QModelIndex)    
    def updateViews(self,item):
        self.dialog.views.setCurrentIndex(item.row())


    @pyqtSlot(dict,str)
    def updateCombo(self,data,name):
        viewable="{ID} - {NAME}".format(**dict(ID=data.get("id"),NAME=data.get("name")))
        getattr(self.dialog,name).items.addItem(viewable)
        #store data for worker for later 
        print(data,name) 
