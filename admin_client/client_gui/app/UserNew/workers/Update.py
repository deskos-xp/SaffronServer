from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import requests,json,ast,os,sys

class UpdateSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()    
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    
    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class Update(QRunnable):
    def __init__(self,auth:dict,data:dict,TYPE:str,user_id:int):
        super(Update,self).__init__()
        self.auth=auth
        self.data=data
        self.TYPE=TYPE
        self.signals=UpdateSignals()
        self.user_id=user_id

    def run(self):
        try:
            auth=(
                self.auth.get("username"),
                self.auth.get("password")
            )
            addr="{server_address}/user/update/{user_id}/add/{TYPE}/{type_id}".format(**dict(server_address=self.auth.get("server_address"),user_id=self.user_id,TYPE=self.TYPE,type_id=self.data.get('id')))
            print(addr,'>'*40)
            response=self.signals.session.get(addr,auth=auth) 
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
