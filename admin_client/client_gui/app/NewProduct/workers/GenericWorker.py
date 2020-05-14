from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QComboBox
import requests,json,ast,os,sys

class WorkerSignals(QObject):
    hasItem:pyqtSignal=pyqtSignal(QComboBox,dict)
    session=requests.Session()
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished=pyqtSignal()

    @pyqtSlot()
    def killMe(self):
        self.kill=True
        self.session.close()

class Worker(QRunnable):
    def __init__(self,auth:dict,objectName:str,combo:QComboBox):
        super(Worker,self).__init__()
        self.combo=combo
        self.signals=WorkerSignals()
        self.Name=objectName
        self.auth=auth

    def run(self):
        auth=(self.auth.get("username"),self.auth.get("password"))
        
        response=self.signals.session.post(
                "{server_address}/{NAME}/get".format(**dict(server_address=self.auth.get("server_address"),NAME=self.Name)),
                auth=auth,
                json=dict(page=0,limit=sys.maxsize)
                )
        if response.status_code == 200:
            try:
                j=response.json()
                if 'objects' in j.keys():
                    objects=j.get('objects')
                    for o in objects:
                        self.signals.hasItem.emit(self.combo,o)
            except Exception as e:
                print(e)
        self.signals.finished.emit()
