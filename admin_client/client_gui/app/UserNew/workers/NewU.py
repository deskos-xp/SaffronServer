from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import requests,json,ast,os,sys

class NewUSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session:requests.Session=requests.Session()

class NewU(QRunnable):
    def __init__(self,auth:dict,user_data:dict,department_data:dict,address_data:dict,role_data:dict):
        self.auth=auth
        self.dataUser=user_data
        self.dataDepartment=department_data
        self.dataAddress=address_data
        self.dataRole=role_data

        self.signals=NewUSignals()

    def run(self):
        try:
            pass
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
