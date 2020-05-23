from PyQt5.QtCore import QThreadPool,QObject,QRunnable,QThread,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import requests,json,ast,os,sys

class CommitToServerSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class CommitToServer(QRunnable):
    def __init__(self,auth:dict,data:dict,TYPE:str):
        super(CommitToServer,self).__init__()
        self.auth=auth
        self.data=data
        self.TYPE=TYPE
        self.signals=CommitToServerSignals()

    def assembleAddressForPost(self) -> str:
        return "{server_address}/{TYPE}/new".format(**dict(server_address=self.auth.get("server_address"),TYPE=self.TYPE))

    def run(self):
        try:
            addr=self.assembleAddressForPost()
            response=self.signals.session.post(addr,json=self.data,auth=(
                self.auth.get("username"),
                self.auth.get("password")
                )
            )
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
            print(e)
        self.signals.finished.emit()
