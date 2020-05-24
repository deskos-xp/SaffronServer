from PyQt5.QtCore import QObject,QThreadPool,QRunnable,QThread,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget

import requests,sys,os,ast,json,re

class UpdateWorkerSignals(QObject):
    killMe:bool=False
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()
    session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class UpdateWorker(QRunnable):
    def __init__(self,auth,addressID,TYPE,entityID):
        super(UpdateWorker,self).__init__()
        self.auth=auth
        self.addressID=addressID.get('ID')
        self.TYPE=TYPE
        self.entityID=entityID
        self.signals=UpdateWorkerSignals()
        self.sendAddress="{server_address}/{TYPE}/update/{entityID}/add/address/{addressID}".format(**dict(server_address=self.auth.get("server_address"),TYPE=self.TYPE,entityID=self.entityID,addressID=self.addressID))

    def run(self):
        try:
            auth=(self.auth.get('username'),self.auth.get('password'))
            response=self.signals.session.get(self.sendAddress,auth=auth)
            self.signals.hasResponse.emit(response)
            print(response.content)
            print(self.sendAddress)
            #exit()
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
