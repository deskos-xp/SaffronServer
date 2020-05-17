from PyQt5.QtWidgets import QWidget,QListView,QCheckBox
from PyQt5.QtCore import QCoreApplication,QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
from PyQt5 import uic
import ast,json,os,sys

from . import mode
from .workers.GetWorker import GetWorker

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
        

    def modeSet(self,state):
        if type(self.sender()) == type(QCheckBox()):
            self.checked[self.sender().objectName()]=state
            getattr(self.widget,'{n}_le'.format(**dict(n=self.sender().objectName()))).setEnabled(state)


    def search(self):
        #print(mode(self.checked),self.checked)
        get=mode(self.checked)
        true_keys=[i for i in self.checked.keys() if self.checked.get(i) == True]
        getURI="{address}/product/get{addon}"

        if get == True:
            data=dict()
            getURI=getURI.format(**dict(address=self.auth.get("server_address"),addon=""))
            for k in true_keys:
                kMod="{k}_le".format(**dict(k=k))
                data[k.lower()]=getattr(self.widget,kMod).text()
            print(data,getURI)
        else:
            if self.widget.ID.isChecked() == True:
                ID=self.widget.ID_le.text()
                getURI=getURI.format(**dict(address=self.auth.get("server_address"),addon="/{ID}".format(**dict(ID=ID))))
            else:
                getURI=getURI.format(**dict(address=self.auth.get("server_address"),addon=""))
            print(getURI)

            '''
            getWorker=GetWorker(self.auth,data)
            getWorker.hasItem.connect(self.itemUpdate)
            getWorker.hasError.connect(self.displayError)
            getWorker.finished.connect(self.stateProgress)
            '''

        def itemUpdate(self,data):
            print(data)

        def displayError(self,error):
            print(error)

        def stateProgress(self):
            print(self.sender(),"state complete")
