from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog
import requests,os,sys,json


class GetComboDataSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasItem:pyqtSignal=pyqtSignal(dict)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class GetComboData(QRunnable):
    def __init__(self,auth:dict,name:str):
        super(GetComboData,self).__init__()
        self.signals=GetComboDataSignals()
        self.auth=auth
        self.name=name

    def run(self):
        try:
            auth=(
                self.auth.get("username"),
                self.auth.get("password")
            )
            addr="{server_address}/{NAME}/get".format(**dict(server_address=self.auth.get("server_address"),NAME=self.name))
            d=dict(page=0,limit=sys.maxsize)
            response=self.signals.session.post(addr,auth=auth,json=d)
            self.signals.hasResponse.emit(response)
            j=response.json()
            stat=j.get('status')
            item=j.get(stat)
            if isinstance(item,dict):
                self.signals.hasItem.emit(item)
            else:
                for i in item:
                    self.signals.hasItem.emit(i)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
