from PyQt5.QtCore import QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog
import requests,os,sys,json,ast

class NewWorkerSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()


class NewWorker(QRunnable):
    def __init__(self,auth:dict,data:dict,TYPE:str):
        super(NewWorker,self).__init__()
        self.TYPE=TYPE
        self.auth=auth
        self.data=data
        self.signals=NewWorkerSignals()

    def run(self):
        try:
            auth=(
                self.auth.get("username"),
                self.auth.get("password")
            )
            address="{server_address}/{TYPE}/new".format(**dict(server_address=self.auth.get("server_address"),TYPE=self.TYPE))
            response=self.signals.session.post(address,json=self.data,auth=auth)
            print(address,'newWorker')
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
    
