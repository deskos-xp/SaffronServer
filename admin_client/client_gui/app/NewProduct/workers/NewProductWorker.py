from PyQt5.QtCore import QThreadPool,QRunnable,QObject,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import requests,os,sys,json,ast

class NewProductWorkerSignals(QObject):
    finished:pyqtSignal=pyqtSignal(bool)
    killMe:bool=False
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasProductId:pyqtSignal=pyqtSignal(int)
    session=requests.Session()
    hasError:pyqtSignal=pyqtSignal(Exception)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class NewProductWorker(QRunnable):
    def __init__(self,auth,data:dict):
        self.auth=auth
        self.data=data
        super(NewProductWorker,self).__init__()
        self.signals=NewProductWorkerSignals()
        self.response:requests.Response=None

    def run(self):
        try:
            self.response=self.signals.session.post("{address}/product/new".format(
                **dict(address=self.auth.get("server_address"))),
                auth=(
                    self.auth.get("username"),
                    self.auth.get("password")
                ),
                json=self.data)
            if self.response != None:
                self.signals.hasResponse.emit(self.response)
                if self.response.json() != None:
                    j=self.response.json()
                    if 'id' in j.keys():
                        self.signals.hasProductId.emit(j.get('id'))
        except Exception as e:
            self.signals.hasError.emit(e)
            print(e)
