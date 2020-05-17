import os,sys,requests,json,ast
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot

class GetWorkerSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasItem:pyqtSignal=pyqtSignal(object)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()


class GetWorker(QRunnable):
    def __init__(self,auth:dict,data:dict,URI:str):
        self.auth=auth
        self.data=data
        self.URI=URI
        self.signals=GetWorkerSignals()
        super(GetWorker,self).__init__()

    def run(self):
        try:
            #do something
            pass
        except Exception as e:
            self.signals.hasError.emit(e)
            print(e)
        self.signals.finished.emit()
