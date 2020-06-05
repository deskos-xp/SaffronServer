from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QWidget
import json,os,sys,requests

from ...common.TableModel import TableModel

class GetUsersSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasUser:pyqtSignal=pyqtSignal(dict)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session:requests.Session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class GetUsers(QRunnable):
    def __init__(self,auth:dict):
        super(GetUsers,self).__init__()
        self.auth=auth
        self.signals=GetUsersSignals()

    def run(self):
        try:
            data=dict(page=0,limit=sys.maxsize)
            auth=(
                self.auth.get("username"),
                self.auth.get("password")
            )
            addr="{server_address}/user/get".format(**dict(server_address=self.auth.get("server_address")))
            response=self.signals.session.post(addr,json=data,auth=auth)
            self.signals.hasResponse.emit(response)
            j=response.json()
            t=j.get("status")
            user=j.get(t)
            print(user)
            if response.status_code == 200:
                if type(user) == type(dict()):
                    self.signals.hasUser.emit(user)
                else:
                    for u in user:
                        self.signals.hasUser.emit(u)
            else:
                raise Exception("return status was {CODE}".format(response.status_code))
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
