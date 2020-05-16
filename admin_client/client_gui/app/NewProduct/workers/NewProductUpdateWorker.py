from PyQt5.QtCore import QThreadPool,QRunnable,QObject,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import requests,os,sys,json,ast

class NewProductUpdateWorkerSignals(QObject):
    finished:pyqtSignal=pyqtSignal()
    killMe:bool=False
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    session=requests.Session()
    hasError:pyqtSignal=pyqtSignal(Exception)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class NewProductUpdateWorker(QRunnable):
    def __init__(self,auth,data:str):
        self.auth=auth
        self.data=data
        super(NewProductUpdateWorker,self).__init__()
        self.signals=NewProductUpdateWorkerSignals()
        self.response:requests.Response=None

    def run(self):
        try:
            self.response=self.signals.session.post(self.data,
                auth=(
                    self.auth.get("username"),
                    self.auth.get("password")
                )
                )
            if self.response != None:
                self.signals.hasResponse.emit(self.response)
        except Exception as e:
            self.signals.hasError.emit(e)
            print(e)
        self.signals.finished.emit()
