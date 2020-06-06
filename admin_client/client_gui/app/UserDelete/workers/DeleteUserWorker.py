from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog
from ...common.Fields import *
import os,sys,json,requests
import colored

class DeleteUserWorkerSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    finished:pyqtSignal=pyqtSignal()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class DeleteUserWorker(QRunnable):
    def __init__(self,auth:dict,user:dict):
        super(DeleteUserWorker,self).__init__()
        self.auth=auth
        self.user=user
        self.signals=DeleteUserWorkerSignals()

    def deleteUser(self,auth:tuple,user_id:int) -> requests.Response:
        addr="{server_address}/user/delete/{id}".format(**dict(server_address=self.auth.get("server_address"),id=user_id))
        response=self.signals.session.delete(addr,auth=auth)
        return response

    def deleteRoleFromUser(self,auth:tuple,user_id:int,role_id:int):
        addr="{server_address}/user/update/{user_id}/remove/roles/{role_id}".format(**dict(server_address=self.auth.get("server_address"),user_id=user_id,role_id=role_id))
        response=self.signals.session.get(addr,auth=auth)
        return response

    def run(self):
        try:
            auth=(
                self.auth.get("username"),
                self.auth.get("password")
            )
            #delete roles
            for entry in self.user.get("roles"):
                response=self.deleteRoleFromUser(auth,self.user.get("id"),entry.get("id"))
                self.signals.hasResponse.emit(response)
            #delete user
            response=self.deleteUser(auth,self.user.get("id"))
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
