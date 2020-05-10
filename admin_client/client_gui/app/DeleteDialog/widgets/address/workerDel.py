from PyQt5.QtCore import QThread,QObject,QRunnable,pyqtSignal,pyqtSlot
import os,sys
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import QListWidget,QListWidgetItem
import requests,ast,json,os,sys

class WorkerDelSignals(QObject):
    kill_bool:bool=False
    done:pyqtSignal=pyqtSignal(int)
    waitResult:bool=False

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
            #not ready for deployment yet
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
            self.signals.done.emit(status_code)
        else:
            print("waiting until address widget is visible")
