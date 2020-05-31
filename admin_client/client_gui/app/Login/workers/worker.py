from PyQt5.QtCore import QThreadPool,QCoreApplication,QObject,QRunnable,pyqtSignal,pyqtSlot
import json,ast,os,sys,requests

from dotenv import load_dotenv

class WorkerSignals(QObject):
    state:pyqtSignal=pyqtSignal(bool)
    user:pyqtSignal=pyqtSignal(dict)
    killMe=False
    hasError:pyqtSignal=pyqtSignal(Exception)

    @pyqtSlot()
    def kill(self):
        self.killMe=True

class Worker(QRunnable):
    def __init__(self,auth):
        self.auth=auth
        super(Worker,self).__init__()
        self.signals=WorkerSignals()
        self.session=requests.Session()

    def run(self):
        try:
            self.status=self.session.post(
                    "{address}/user/get".format(address=self.auth.get("server_address")),
                    auth=(self.auth.get("username"),
                        self.auth.get("password")),
                    json=dict(page=0,limit=1,uname=self.auth.get("username")))
            try:
                print(self.status.json())
                j=self.status.json()
                if 'objects' in j:
                    uList=j.get('objects')
                    if uList != None and len(uList) > 0:
                        self.signals.user.emit(uList[0])
                        self.signals.state.emit(True)
                    else:
                        self.signals.state.emit(False)
                else:
                    self.signals.state.emit(False)
            except Exception as e:
                self.signals.state.emit(False)
                print(e)
        except Exception as e:
            self.signals.hasError.emit(e)
