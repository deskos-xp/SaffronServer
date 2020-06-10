from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json,ast,requests
from ...common.Fields import *

class SaveRelationsSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class SaveRelations(QRunnable):
    def __init__(self,auth:dict,data:dict,cached:dict,name:str,name_whom:str):
        super(SaveRelations,self).__init__()
        self.auth=auth
        self.data=keyStripper('NAME',data)
        self.name=name
        self.name_whom=name_whom
        self.signals=SaveRelationsSignals()
        print(cached)
        if cached != None:
            if len(cached) > 0:
                self.cached=cached[0]
            else:
                self.cached={}
        else:
            self.cached={}

    def run(self):
        try:
            auth=(
                    self.auth.get("username"),
                    self.auth.get("password")
                    )
            print(self.cached,"$"*30)
            if self.cached != {}:
                rm_addr="{server_address}/{NAME}/update/remove/{E}/{ID}".format(**dict(server_address=self.auth.get("server_address"),NAME=self.name,ID=self.cached.get("id"),E=self.name_whom))
                print(rm_addr)
            addr="{server_address}/{NAME}/update/add/{E}/{ID}".format(**dict(server_address=self.auth.get("server_address"),NAME=self.name,ID=self.data.get("id"),E=self.name_whom))
            print(addr)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
