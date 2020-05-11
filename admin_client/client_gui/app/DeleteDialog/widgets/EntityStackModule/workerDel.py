from PyQt5.QtCore import QThread,QObject,QRunnable,pyqtSignal,pyqtSlot
import os,sys
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import QListWidget,QListWidgetItem
import requests,ast,json,os,sys

class WorkerDelSignals(QObject):
    kill_bool:bool=False
    done:pyqtSignal=pyqtSignal(int,int)
    waitResult:bool=False
    ID:int=None
    
    @pyqtSlot(int)
    def setID(self,ID:int):
        self.ID=ID

    @pyqtSlot(bool)
    def wait(self,func):
        self.waitResult=func

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

    def run(self):
        if self.signals.waitResult == False:
            #dummy code
            status_code=200
            if self.signals.kill_bool == True:
                return
            #not ready for deployment yet
            #print(self.signals.ID)
            #print("{address}/{parent_name}/delete/{ID}".format(**dict(address=self.address,ID=self.signals.ID,parent_name=self.parent_name))) 
            #exit(1)
            status=requests.delete("{address}/{parent_name}/delete/{ID}".format(**dict(address=self.address,ID=self.signals.ID,parent_name=self.parent_name)),auth=self.auth)
            status_code=status.status_code

            self.signals.done.emit(status_code,self.signals.ID)
        else:
            print("waiting until {parent_name} widget is visible".format(**dict(parent_name=self.parent_name)))
