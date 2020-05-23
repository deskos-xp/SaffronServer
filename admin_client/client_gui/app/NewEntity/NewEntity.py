from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QThread,QObject,QRunnable,pyqtSignal,QModelIndex,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog,QHeaderView
import os,sys,json,ast,requests

from .NewEntityListModel import NewEntityListModel
from .NewEntityTableModel import NewEntityTableModel
from .workers.CommitToServer import CommitToServer
class SaveEntity(QObject):
    updateAll:pyqtSignal=pyqtSignal()
    def __init__(self,obj,auth:dict,TYPE:str):
        super(SaveEntity,self).__init__()
        self.obj=obj
        self.auth=auth
        self.TYPE=TYPE
        model=obj.model()
        print(model)
    @pyqtSlot()
    def update(self):
        self.updateAll.emit()

    @pyqtSlot()
    def createWorker(self):
        #print(self.obj.model().item)
        self.worker=CommitToServer(self.auth,self.obj.model().item,self.TYPE)
        self.worker.signals.hasResponse.connect(self.displayResponse)
        self.worker.signals.hasError.connect(self.displayError)
        self.worker.signals.finished.connect(self.update)

    @pyqtSlot()
    def commission(self):
        QThreadPool.globalInstance().start(self.worker)
        #notify other workers to update comboboxs
        #need to add a way to add address to vendor,brand,manufacturer entities -- screw that use self.updateAll.emit() signal

    @pyqtSlot(Exception)
    def displayError(self,error:Exception):
        print(error)

    @pyqtSlot(requests.Response)
    def displayResponse(self,response):
        print(response)

    @pyqtSlot(bool)
    def display(self,state):
        print(self.obj.model().item)
        self.createWorker()
        self.commission()

class NewEntity(QDialog):
    def update(self):
        self.parent.newGrid.initialize(re=True)

    def __init__(self,auth:dict,parent):
        super(NewEntity,self).__init__()
        self.auth=auth
        self.dialog=QDialog()
        self.parent=parent

        uic.loadUi("app/NewEntity/forms/NewEntity.ui",self.dialog)

        self.types=["address","vendor","brand","manufacturer","department"]
        self.model=NewEntityListModel()
        self.dialog.types_view.setModel(self.model)
        self.model.items=self.types
        self.model.layoutChanged.emit()

        self.dialog.types_view.activated.connect(self.itemActivated)
        #set default page
        self.dialog.types_widget.setCurrentIndex(0)
        self.dialog.TYPE.setText(self.types[0])
        self.dialog.confirm.rejected.connect(self.dialog.reject)
        self.savers=dict()

        self.models=dict()
        for i in self.types:
            uic.loadUi("app/NewEntity/forms/NewEntityItem.ui",getattr(self.dialog,i))
            getattr(self.dialog,i).progressBar.hide()
            self.models[i]=NewEntityTableModel()
            self.savers[i]=SaveEntity(getattr(self.dialog,i).tableView,self.auth,i)
            self.savers[i].updateAll.connect(self.update)

            getattr(self.dialog,i).tableView.setModel(self.models[i])
            getattr(self.dialog,i).tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            getattr(self.dialog,i).tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            getattr(self.dialog,i).save.clicked.connect(self.savers[i].display)

            self.models[i].load_data(self.fields(i))
            self.models[i].layoutChanged.emit()

        #worker to send data to server
        #need progress bar

        self.dialog.exec_()

    def fields(self,name):
        def addressFields():
            return dict(
                    city="",
                    state="",
                    street_number="",
                    street_name="",
                    ZIP="",
                    apartment_suite=""
                    )
        def genericFields():
            return dict(
                comment="",
                name="",
                email="",
                phone=""
                    )
        if name == 'address':
            return addressFields()
        else:
            return genericFields()

    def itemActivated(self,index):
        self.dialog.types_widget.setCurrentIndex(index.row())
        self.dialog.TYPE.setText(self.types[index.row()])
