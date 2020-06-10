from PyQt5.QtCore import QObject,QRunnable,QThread,pyqtSignal,pyqtSlot
import os,sys,json,requests


class ULookupSearchSignal(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasUser:pyqtSignal=pyqtSignal(dict,str)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal(str)
    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()


class ULookupSearch(QRunnable):
    def __init__(self,auth:dict,terms:dict,**kwargs):
        super(ULookupSearch,self).__init__()
        self.auth=auth
        self.terms=terms
        self.signals=ULookupSearchSignal()
        self.name=kwargs.get("name")

    def run(self):
        try:
            auth=(
                self.auth.get("username"),
                self.auth.get("password")
            )
            comp=dict(server_address=self.auth.get("server_address"))
            addr="{server_address}/user/get".format(**comp)
            response=self.signals.session.post(addr,auth=auth,json=self.terms)
            self.signals.hasResponse.emit(response)
            if response.status_code == 200:
                j=response.json()
                stat=j.get("status")
                users=j.get(stat)
                if isinstance(users,list):
                    for u in users:
                        self.signals.hasUser.emit(u,self.name)
                else:
                    self.signals.hasUser.emit(user,self.name)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit(self.name)
