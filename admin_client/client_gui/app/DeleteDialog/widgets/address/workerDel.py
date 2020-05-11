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
    def __init__(self,auth,address):
        super(WorkerDel,self).__init__()
        self.signals=WorkerDelSignals()
        self.auth=auth
        self.address=address
        
    def run(self):
        if self.signals.waitResult == False:
            #dummy code
            status_code=200
            if self.signals.kill_bool == True:
                return
            #not ready for deployment yet
            print(self.signals.ID)
            
            status=requests.delete("{address}/address/delete/{ID}".format(**dict(address=self.address,ID=self.signals.ID)),auth=self.auth)
            status_code=status.status_code

            '''
            
            while self.signals.kill_bool == False:
                data=dict(page=0,limit=sys.maxsize)
                response=requests.post("{address}/address/get".format(**dict(address=self.address)),auth=self.auth,json=data)
                if response.status_code == 200:
                    try:
                        j=response.json()
                        if 'objects' in j.keys():
                            j=j['objects']
                            for k in j:
                                self.signals.ready.emit(k)
                    except Exception as e:
                        print(e)
                #self.signals.ready.emit(dict())
                QThread.sleep(2)  
            '''
            self.signals.done.emit(status_code,self.signals.ID)
        else:
            print("waiting until address widget is visible")
