from PyQt5.QtCore import QObject,QRunnable,pyqtSignal,pyqtSignal,QThreadPool,pyqtSlot,QModelIndex
from PyQt5.QtWidgets import QWidget,QDialog,QListView,QStackedWidget,QComboBox,QHeaderView,QTableView

import os,sys,json,ast,requests,re
from PyQt5 import uic
from .DeleteDialogModel import DeleteDialogModel
from .DeleteDialogTableModel import DeleteDialogTableModel
from .workers.GetComboData import GetComboData
from .workers.DeleteWorker import DeleteWorker
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
        self.models=dict()
        self.datas=dict()
        self.workers=dict()

        for i in self.items:
            uic.loadUi("app/DeleteDialog_rev2/forms/DeleteDialogItemView.ui",getattr(self.dialog,i.lower()))
            self.datas[i.lower()]=list()
            self.models[i.lower()]=DeleteDialogTableModel()
            getattr(self.dialog,i.lower()).dataView.setModel(self.models[i.lower()])

            getattr(self.dialog,i.lower()).dataView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            getattr(self.dialog,i.lower()).dataView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            getattr(self.dialog,i.lower()).setObjectName(i.lower())
            getattr(self.dialog,i.lower()).entityName.setText(i[0].upper()+i[1:])
            getattr(self.dialog,i.lower()).confirm.rejected.connect(self.dialog.reject)
            getattr(self.dialog,i.lower()).confirm.accepted.connect(self.DeleteFromServer)
            
            #QComboBox.currentIndexChanged()
            getattr(self.dialog,i.lower()).items.activated.connect(self.updateViewer)

            self.workers[i.lower()]=GetComboData(self.auth,i.lower())
            self.workers[i.lower()].signals.hasError.connect(lambda x:print(x))
            self.workers[i.lower()].signals.hasItems.connect(self.updateCombo)

            QThreadPool.globalInstance().start(self.workers[i.lower()])

            #update from worker


        self.dialog.exec_()

    def regexThisShit2(self,text):
        try:
            p=re.search("(?P<ID>\d*):(?P<TYPE>\w*)",text)
            return dict(ID=p.group("ID"),TYPE=p.group("TYPE"))
        except Exception as e:
            print(e)

    def regexThisShit(self,text):
        try:
            p=re.compile('^\d*:\w*')
            result=p.match(text)
            s2=result.group()

            p=re.compile('^\d*:')
            ID=p.match(s2)
            ID=int(ID.group()[:-1])

            p=re.compile(':[\w]*')
            TYPE=p.search(s2).group()
            TYPE=TYPE[1:]
            return dict(ID=ID,TYPE=TYPE)
        except Exception as e:
            print(e)

    def preRegex(self,text):
        ID=text.split(" - ")[0]
        TYPE=ID.split(":")[1]
        ID=ID.split(":")[0]
        return dict(ID=ID,TYPE=TYPE)


    def DeleteFromServer(self):
        offspring=self.sender().parent().children()
        for child in offspring:
            if type(child) == type(QTableView()):
                mod=child.model()
                #clear model
            if type(child) == type(QComboBox()):
                text=child.currentText()
                tmp=self.regexThisShit2(text)
                ID=tmp.get('ID')
                TYPE=tmp.get('TYPE')
                del_address="{server_address}/{TYPE}/delete/{ID}".format(**dict(server_address=self.auth.get("server_address"),TYPE=TYPE,ID=ID))
                #delete worker needs to be made
                print(del_address)
                deleteMe=DeleteWorker(self.auth,del_address)
                deleteMe.signals.hasResponse.connect(self.responseRecieved)
                deleteMe.signals.hasError.connect(lambda x:print(e))
                
                QThreadPool.globalInstance().start(deleteMe)
                #on worker finished do below
                self.dialog.accept()

    @pyqtSlot(requests.Response)
    def responseRecieved(self,response):
        if response.status_code != 200:
            print("it seems that something went wrong")
            print(response)
        self.dialog.accept()

    def updateViewer(self,index):
        ID=self.sender().currentText().split(" - ")[0]
        TYPE=ID.split(":")[1]
        ID=ID.split(":")[0]
        for i in self.datas[TYPE]:
            if i.get('id') and i.get('id') == int(ID):
                self.models[TYPE].load_data(i)
                self.models[TYPE].layoutChanged.emit()        
                break

    @pyqtSlot(QModelIndex)    
    def updateViews(self,item):
        self.dialog.views.setCurrentIndex(item.row())

    @pyqtSlot(dict,str)
    def updateCombo(self,data,name):
        viewable="{ID}:{name} - {NAME}".format(**dict(ID=data.get("id"),name=name,NAME=data.get("name")))
        #print(self.regexThisShit2(viewable))
        getattr(self.dialog,name).items.addItem(viewable)
        #store data for worker for later 
        #print(name)
        if data not in self.datas[name]:
            self.datas[name].append(data)
