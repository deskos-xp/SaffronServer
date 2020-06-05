from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog
from ...common.Fields import *
import os,sys,json,requests


class DeleteUserWorkerSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    finished:pyqtSignal=pyqtSignal()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class DeleteUserWorker(QRunnable):
    def __init__(self,auth:dict,user:dict):
        super(DeleteUserWorker,self).__init__()
        self.auth=auth
        self.user=user
        self.signals=DeleteUserWorkerSignals()
    def run(self):
        try:
            auth=(
                self.auth.get("username"),
                self.auth.get("password")
            )
            addr="{server_address}/user/delete/{id}".format(**dict(server_address=self.auth.get("server_address"),id=self.user.get("id")))
            response=self.signals.session.delete(addr,auth=auth) 
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
