from PyQt5.QtCore import QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
import requests,os,sys,ast,json
from ...common.Fields import *

class UpdateADSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session=requests.Session()
    disabledGrid:pyqtSignal=pyqtSignal(bool)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()


class UpdateAD(QRunnable):
    def __init__(self,auth:dict,data:dict,identifier:int,name:str):
        super(UpdateAD,self).__init__()
        self.auth=auth
        self.data=data
        self.identifier=identifier
        self.name=name
        self.signals=UpdateADSignals()
        self.old=dict(data)

    def run(self):
        self.signals.disabledGrid.emit(False)
        self.data=stripStructures(self.data)
        auth=(
            self.auth.get('username'),
            self.auth.get('password')
                )
        addr="{server_address}/{name}/update/{ID}".format(
                **dict(
                    server_address=self.auth.get("server_address"),
                    name=self.name,
                    ID=self.data.get('id')
                    ))
        print(addr)
        try:
            print("[worker data]",self.data)
            response=self.signals.session.post(addr,auth=auth,json=self.data)
            self.signals.hasResponse.emit(response)
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)
            self.signals.kill()
        self.signals.disabledGrid.emit(True)
        self.signals.finished.emit()
