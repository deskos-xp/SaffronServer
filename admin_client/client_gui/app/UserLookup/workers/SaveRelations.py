from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json,ast,requests
from ...common.Fields import *

class SaveRelationsSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class SaveRelations(QRunnable):
    def __init__(self,auth:dict,data:dict):
        super(SaveRelations,self).__init__()
        self.auth=auth
        self.data=data
        self.signals=SaveRelationsSignals()

    def run(self):
        try:
            pass
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
