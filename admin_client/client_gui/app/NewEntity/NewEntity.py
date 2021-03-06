from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QThread,QObject,QRunnable,pyqtSignal,QModelIndex,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog,QHeaderView
import os,sys,json,ast,requests,re

from .NewEntityListModel import NewEntityListModel
from .NewEntityTableModel import NewEntityTableModel
from .workers.CommitToServer import CommitToServer
from .workers.GetComboData import GetComboData
from .workers.UpdateWorker import UpdateWorker
from ..common.Fields import *

class SaveEntity(QObject):
    updateAll:pyqtSignal=pyqtSignal()
    complete:pyqtSignal=pyqtSignal()
    def __init__(self,obj,auth:dict,TYPE:str,parent,dialog):
        super(SaveEntity,self).__init__()
        self.obj=obj
        self.auth=auth
        self.TYPE=TYPE
        self.parent=parent
        self.dialog=dialog
        self.addressID=None
        self.entityID=None

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

    def updateWorker(self):
        if self.entityID == None:
            return
        if self.addressID == None:
            return
        print(self.addressID,self.entityID)
        
        self.update_worker=UpdateWorker(self.auth,self.addressID,self.TYPE,self.entityID)
        self.update_worker.signals.hasResponse.connect(self.displayResponseUpdate)
        self.update_worker.signals.hasError.connect(self.displayError)
        self.update_worker.signals.finished.connect(self.update)
        QThreadPool.globalInstance().start(self.update_worker)
        

    @pyqtSlot()
    def commission(self):
        QThreadPool.globalInstance().start(self.worker)
        #notify other workers to update comboboxs
        #need to add a way to add address to vendor,brand,manufacturer entities -- screw that use self.updateAll.emit() signal

    @pyqtSlot(Exception)
    def displayError(self,error:Exception):
        print(error)


    @pyqtSlot(requests.Response)
    def displayResponseUpdate(self,response):
        print(response)
        #self.complete.emit()
        self.parent.progressBar.hide()

    @pyqtSlot(requests.Response)
    def displayResponse(self,response):
        print(response,'*'*60)
        if self.TYPE not in ['address','department']:
            try:
                if response.json() != None and 'id' in response.json().keys():
                    self.entityID=response.json().get('id')
                    self.updateWorker()
            except Exception as e:
                print(e)
        self.parent.progressBar.hide()
        self.complete.emit()

    def regexThisShit2(self,text):
        try:
            p=re.search("(?P<ID>\d*) -",text)
            return dict(ID=p.group("ID"))
        except Exception as e:
            print(e)
        return 

    @pyqtSlot(bool)
    def display(self,state):
        self.parent.progressBar.show()
        #print(self.obj.model().item)
        self.createWorker()
        self.commission()
        self.addressID=self.regexThisShit2(self.parent.addresses.currentText())
        print(self.addressID)

    @pyqtSlot(bool)
    def resetView(self,state):
        self.obj.model().load_data(NewEntity.fields(self,self.TYPE))
        self.obj.model().layoutChanged.emit()

    @pyqtSlot(bool)
    def handle_new_address(self,state):
        print(self.sender().parent().parent().parent().objectName(),state)
        self.next()
 
    @pyqtSlot(bool)
    def status_first(self,state):
        print(self.TYPE)

    def back(self):
        self.dialog.stackedWidget.setCurrentIndex(0)
    
    def next(self):
        self.dialog.stackedWidget.setCurrentIndex(1)

    '''
    if addresses combo has a selected address:
        do update
    else:
        pass
    '''
    ####
    '''for saving address:
            get id after save
            do update method for TYPE
    '''

class NewEntity(QDialog):
    @pyqtSlot()
    def update(self): 
        self.parent.newGrid.initialize(re=True)
        for i in self.types:
            try:
                pass
                #print(getattr(self.parent.newGrid,i).itemData,'data'*4)
            except:
                pass
        for i in self.types:
            self.prepCombos(i,re=True)

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

        def back(state):
            SaveEntity.back(self)

        self.comboWorkers=dict()

        self.models=dict()
        self.address_tmp=dict()

        for i in self.types:
            self.address_tmp[i]=list()
            self.comboWorkers[i]=GetComboData(self.auth,'address')

        self.prepCombos("vendor")
        self.prepCombos("brand")
        self.prepCombos("manufacturer")


        for i in self.types:
            uic.loadUi("app/NewEntity/forms/NewEntityItem.ui",getattr(self.dialog,i))
            getattr(self.dialog,i).progressBar.hide()
            self.models[i]=NewEntityTableModel()
            self.savers[i]=SaveEntity(getattr(self.dialog,i).tableView,self.auth,i,getattr(self.dialog,i),self.dialog)
            self.savers[i].updateAll.connect(self.update)
            
            if i not in  ['address','department']:
                pass
            else:
                getattr(self.dialog,i).addresses.setEnabled(False)
                getattr(self.dialog,i).addresses.hide()

            getattr(self.dialog,i).setObjectName(i)
            #worker address updater
            getattr(self.dialog,i).tableView.setModel(self.models[i])
            getattr(self.dialog,i).tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            getattr(self.dialog,i).tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            getattr(self.dialog,i).save.clicked.connect(self.savers[i].display)
            getattr(self.dialog,i).clear.clicked.connect(self.savers[i].resetView)
            self.models[i].load_data(fields(i))
            self.models[i].layoutChanged.emit()

        #worker to send data to server
        #need progress bar

        self.dialog.exec_()
        
    def prepCombos(self,name,re=False):
        if re == True:
            self.address_tmp[name]=list()
            self.comboWorkers[name]=GetComboData(self.auth,'address')

        self.comboWorkers[name].signals.hasItems.connect(lambda x,n: self.updateCombo(name,x))
        self.comboWorkers[name].signals.hasError.connect(lambda x: print(x))
        QThreadPool.globalInstance().start(self.comboWorkers[name])


    def updateCombo(self,name,data):
        if toAddressString(data) not in self.address_tmp[name]:
            self.address_tmp[name].append(toAddressString(data))
        getattr(self.dialog,name).addresses.clear()
        getattr(self.dialog,name).addresses.addItems(self.address_tmp[name])

    def itemActivated(self,index):
        self.dialog.types_widget.setCurrentIndex(index.row())
        self.dialog.TYPE.setText(self.types[index.row()])
