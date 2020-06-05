from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog

import requests,json,ast,os,sys


class getADRWorkerSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasADR:pyqtSignal=pyqtSignal(dict)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session:requests.Session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.sessions.close()

class getADRWorker(QRunnable):
    def __init__(self,auth:dict,TYPE:str):
        super(getADRWorker,self).__init__()
        self.auth=auth
        self.TYPE=TYPE
        self.signals=getADRWorkerSignals()

    def run(self):
        try:
            post=dict(page=0,limit=sys.maxsize)
            addr="{server_address}/{TYPE}/get".format(**dict(server_address=self.auth.get("server_address"),TYPE=self.TYPE))
            auth=(
                self.auth.get('username'),
                self.auth.get('password')
                    )
            response=self.signals.session.post(addr,auth=auth,json=post)
            self.signals.hasResponse.emit(response)
            if response.status_code == 200:
                stat=response.json()
                address=stat.get(stat.get("status"))
                print(address)
                for a in address:
                    self.signals.hasADR.emit(a)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
