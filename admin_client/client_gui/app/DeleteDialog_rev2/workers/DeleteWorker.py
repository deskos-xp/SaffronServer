from PyQt5.QtCore import QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import requests,json,os,sys,ast

class DeleteWorkerSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class DeleteWorker(QRunnable):
    def __init__(self,auth:dict,delete_address:str):
        super(DeleteWorker,self).__init__()
        self.auth=auth
        self.delete_address=delete_address
        self.signals=DeleteWorkerSignals()

    def run(self):
        try:
            response=self.signals.session.delete(self.delete_address,auth=(self.auth.get("username"),self.auth.get("password")))
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
            print(e)
        self.signals.finished.emit()
