from PyQt5.QtWidgets import QWidget,QListView,QCheckBox
from PyQt5.QtCore import QCoreApplication,QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot,QTimer,QModelIndex
from PyQt5 import uic
import ast,json,os,sys,enum

from . import mode
from .workers.GetWorker import GetWorker
from . import SearchModeEnum
from .SearchViewModel import SearchViewModel
from ..DataView.DataViewDialog import DataViewDialog
import copy

class SearchProduct(QWidget):
    def __init__(self,auth:dict,widget:QWidget):
        self.widget=widget
        self.auth=auth

        super(SearchProduct,self).__init__()
        
        uic.loadUi("app/SearchProduct/forms/SearchProduct.ui",self.widget)
        self.checked=dict(UPC=False,name=False,home_code=False,ID=False)
        self.widget.ID.toggled.connect(self.modeSet)
        self.widget.home_code.toggled.connect(self.modeSet)
        self.widget.name.toggled.connect(self.modeSet)
        self.widget.UPC.toggled.connect(self.modeSet)

        self.widget.search.clicked.connect(self.search)

        self.model=SearchViewModel()
        self.widget.listView.setModel(self.model)
        self.widget.listView.clicked.connect(self.showData)
        
        self.widget.page.valueChanged.connect(self.searchWrap)
        self.widget.limit.valueChanged.connect(self.searchWrap)
    
        self.widget.progressBar.hide()
        self.widget.progressBar.setMaximum(self.widget.limit.value())

        self.widget.back.clicked.connect(self.SearchWrapMinus)
        self.widget.next.clicked.connect(self.SearchWrapPlus)

        self.qtp=QThreadPool.globalInstance() 
        self.backControlled()

        ''' 
        self.updateTimer:QTimer=QTimer()
        self.updateTimer.setInterval(500)
        self.updateTimer.timeout.connect(self.updateModel)
        self.updateTimer.start()
               

    def updateModel(self):
        print("updating model {count}".format(**dict(count=len(self.model.items))))
        self.model.layoutChanged.emit()
    '''
    @pyqtSlot()
    def backControlled(self):
        if self.widget.page.value() < 1:
            self.widget.back.setEnabled(False)
        else:
            self.widget.back.setEnabled(True)
    
    @pyqtSlot()
    def nextControlled(self,data):
        #print(data)
        if not data:
            self.widget.next.setEnabled(False)
            self.widget.page.setValue(self.widget.page.value()-1)
        else:
            self.widget.next.setEnabled(True)

    @pyqtSlot()
    def SearchWrapMinus(self):
        self.widget.page.setValue(self.widget.page.value()-1)
        self.searchWrap()

    @pyqtSlot()
    def SearchWrapPlus(self):
        self.widget.page.setValue(self.widget.page.value()+1)
        self.searchWrap()

    @pyqtSlot()
    def searchWrap(self):
        #so debugging can be perf'd
        #self.progressBar.setMaximum(self.widget.limit.value())
        #print(len(self.model.items))
        self.backControlled()
        self.search()

    @pyqtSlot(QModelIndex)
    def showData(self,item):
        if self.model.items[item.row()] in [None,{}]:
            self.clearModel()
        else:
            #print(item)
            pkt=dict()
            #it=copy.deepcopy(self.model.items[item.row()])
            #print(it,"iiittt")
            for removeable in self.model.items[item.row()].keys():
                #print(removeable,"*"*3+" removeable")
                if removeable in ['departments','vendors','brands','manufacturers']:
                    print(removeable,"removeable {}".format("*"*30))
                    #it.__delitem__(removeable)
                    pkt[removeable]=self.model.items[item.row()]

            #self.model.items[item.row()]=it
            print(pkt.keys(),"*/*"*33)
            self.dialog=DataViewDialog(self.auth,self.model.items[item.row()],pkt,self)
            #dialog.exec_()
            #now its time for the dataview dialog to be made
        #print(self.model.items[item.row()])

    def modeSet(self,state):
        if type(self.sender()) == type(QCheckBox()):
            self.checked[self.sender().objectName()]=state
            getattr(self.widget,'{n}_le'.format(**dict(n=self.sender().objectName()))).setEnabled(state)

    def search(self):
        self.widget.progressBar.show()
        self.clearModel()
        #print(mode(self.checked),self.checked)
        get=mode(self.checked)
        true_keys=[i for i in self.checked.keys() if self.checked.get(i) == True]
        getURI="{address}/product/get{addon}"
        method=SearchModeEnum.DEFAULT
        data=dict(page=self.widget.page.value(),limit=self.widget.limit.value())
        if get == True:
            getURI=getURI.format(**dict(address=self.auth.get("server_address"),addon=""))
            for k in true_keys:
                kMod="{k}_le".format(**dict(k=k))
                data[k.lower()]=getattr(self.widget,kMod).text()
            method=SearchModeEnum.POST
        else:
            if self.widget.ID.isChecked() == True:
                method=SearchModeEnum.GET
                ID=self.widget.ID_le.text()
                if ID != "":
                    getURI=getURI.format(**dict(address=self.auth.get("server_address"),addon="/{ID}".format(**dict(ID=ID))))
                else:
                    method=SearchModeEnum.DEFAULT
            else:
                method=SearchModeEnum.POST
                getURI=getURI.format(**dict(address=self.auth.get("server_address"),addon=""))
        #print(getURI,data,method)
            
        if method != SearchModeEnum.DEFAULT:
            getWorker=GetWorker(self.auth,data,getURI,method)
            getWorker.signals.hasItem.connect(self.itemUpdate)
            getWorker.signals.hasError.connect(self.displayError)
            getWorker.signals.finished.connect(self.stateProgress)
            self.qtp.start(getWorker)

        #self.nextControlled(self.model.items)    

    @pyqtSlot()
    def clearModel(self):
        self.model.items.clear()
        self.model.layoutChanged.emit()

    def delete(self):
        indexes = self.widget.listView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.items[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.widget.listView.clearSelection()

    @pyqtSlot(dict)
    def itemUpdate(self,data):
        print("----------------->",self.widget.progressBar.value())
        self.widget.progressBar.setValue(self.widget.progressBar.value()+1)
        
        if data == {}:
            self.model.items.clear()
            self.model.layoutChanged.emit()
        elif data not in self.model.items:
            self.model.items.append(data)
            self.model.layoutChanged.emit()

    @pyqtSlot(Exception)
    def displayError(self,error):
        print(error)

    @pyqtSlot()
    def stateProgress(self):
        self.widget.progressBar.hide()
        self.widget.progressBar.setValue(0)
        print(self.sender(),"state complete")
        self.nextControlled(self.model.items)    

