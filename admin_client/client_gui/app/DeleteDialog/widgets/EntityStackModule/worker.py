from PyQt5.QtCore import QThread,QObject,QRunnable,pyqtSignal,pyqtSlot
import os,sys
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import QListWidget,QListWidgetItem
import requests,ast,json,os,sys

class WorkerSignals(QObject):
    #def __init__(self):
    #    super(UpdateSelectorSignals,self).__init__()
    ready:pyqtSignal=pyqtSignal(dict)
    kill_bool:bool=False
    waitResult:bool=True

    @pyqtSlot(bool)
    def wait(self,func): 
        self.waitResult=func

    @pyqtSlot()
    def kill(self):
        self.kill_bool=True

class Worker(QRunnable):
    address:str=None
    auth:tuple=None
    def __init__(self,auth:tuple,address:str,name:str):
        super(Worker,self).__init__()
        self.signals=WorkerSignals()
        self.auth=auth
        self.address=address
        self.parent_name=name
        
    def run(self):
        while self.signals.kill_bool == False:
            print(self.signals.waitResult)
            if self.signals.waitResult == False:
                data=dict(page=0,limit=sys.maxsize)
                #print(self.address)
                #exit(1)
                response=requests.post("{address}/{parent_name}/get".format(**dict(address=self.address,parent_name=self.parent_name)),auth=self.auth,json=data)
                if response.status_code == 200:
                    try:
                        j=response.json()
                        if 'objects' in j.keys():
                            j=j['objects']
                            for k in j:
                                if self.signals.kill_bool == True:
                                    break
                                self.signals.ready.emit(k)
                    except Exception as e:
                        print(e)
                #self.signals.ready.emit(dict())
            else:
                print("Waiting until {parent_name} widget is visible".format(**dict(parent_name=self.parent_name)))
            QThread.sleep(2)    
