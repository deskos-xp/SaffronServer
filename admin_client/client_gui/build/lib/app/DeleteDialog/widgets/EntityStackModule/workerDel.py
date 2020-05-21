from PyQt5.QtCore import QThread,QObject,QRunnable,pyqtSignal,pyqtSlot
import os,sys
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import QListWidget,QListWidgetItem
import requests,ast,json,os,sys

class WorkerDelSignals(QObject):
    kill_bool:bool=False
    done:pyqtSignal=pyqtSignal(int,int)
    ID:int=None
    
    @pyqtSlot(int)
    def setID(self,ID:int):
        self.ID=ID

    @pyqtSlot()
    def kill(self):
        self.kill_bool=True

class WorkerDel(QRunnable):
    address:str=None
    auth:tuple=None
    def __init__(self,auth:tuple,address:str,name:str):
        super(WorkerDel,self).__init__()
        self.signals=WorkerDelSignals()
        self.auth=auth
        self.address=address
        self.parent_name=name
        self.session=requests.Session()
    def run(self):
        status_code=200
        if self.signals.kill_bool == True:
            return
        #not ready for deployment yet
        #print(self.signals.ID)
        #print("{address}/{parent_name}/delete/{ID}".format(**dict(address=self.address,ID=self.signals.ID,parent_name=self.parent_name))) 
        #exit(1)
        url="{address}/{parent_name}/delete/{ID}".format(**dict(address=self.address,ID=self.signals.ID,parent_name=self.parent_name))
        print(url,self.auth)
        status=self.session.delete(url,auth=self.auth)
        status_code=status.status_code
        print(status.text)
        if self.signals.kill_bool == True:
            self.session.close()
        self.signals.done.emit(status_code,self.signals.ID)

