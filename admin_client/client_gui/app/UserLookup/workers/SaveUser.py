from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json,ast,requests
from ...common.Fields import *

class SaveUserSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class SaveUser(QRunnable):
    def __init__(self,auth:dict,data:dict,user_id:int,name:str):
        super(SaveUser,self).__init__()
        self.auth=auth
        self.NAME=data.get('NAME')
        self.data=keyStripper('NAME',data)
        self.user_id=user_id
        self.name=name
        self.signals=SaveUserSignals()

    def run(self):
        try:
            print(self.data,self.user_id,self.name)
            auth=(
                self.auth.get("username"),
                self.auth.get("password")
                    )
            addr="{server_address}/{NAME}/update/{ID}".format(**dict(server_address=self.auth.get('server_address'),NAME=self.name,ID=self.user_id))
            response=self.signals.session.post(addr,auth=auth,json=self.data)
            self.signals.hasResponse.emit(response)
            print(addr,"-l-"*30)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
