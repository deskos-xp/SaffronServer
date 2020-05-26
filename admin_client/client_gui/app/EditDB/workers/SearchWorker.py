from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog
import requests,json,ast,os,sys

class SearchWorkerSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasItems:pyqtSignal=pyqtSignal(list)
    hasItem:pyqtSignal=pyqtSignal(dict)
    hasError:pyqtSignal=pyqtSignal(Exception)

    session:requests.Session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class SearchWorker(QRunnable):
    def __init__(self,auth:dict,data,name:str,defaults:dict):
        super(SearchWorker,self).__init__()
        self.data=data
        self.name=name
        self.auth=auth
        self.signals=SearchWorkerSignals()
        self.defaults=defaults

    def run(self):
        try:
            for k in self.defaults.keys():
                if self.data.get(k) != None:
                    if self.data.get(k) == self.defaults.get(k):
                        self.data.__delitem__(k)
                        #print(k,'# res #')
            address="{server_address}/{TYPE}/get".format(**dict(server_address=self.auth.get("server_address"),TYPE=self.name))
            auth=(self.auth.get("username"),self.auth.get("password"))
            #print(address,auth)
            response=self.signals.session.post(address,auth=auth,json=self.data)
            #print(self.data,self.defaults,'### Search Worker ###',sep="\n")
            if response.status_code == 200:
                if 'status' in response.json():
                    s=response.json().get('status')
                    if s == "objects":
                        self.signals.hasItems.emit(response.json().get(s))
                    elif s == 'object':
                        self.signals.hasItem.emit(response.json().get(s))
                    else:
                        raise Exception("not a valid type {s}".format(**dict(s=s)))
            else:
                raise Exception("return status not 200: {status}".format(**dict(status=response.status_code)))
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()


