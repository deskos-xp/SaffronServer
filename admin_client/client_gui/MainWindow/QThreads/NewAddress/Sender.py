from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
import requests,time,sys,os

class Sender(QThread):
    auth:tuple=None
    address:str=None
    statusSig:pyqtSignal=pyqtSignal(requests.Response)
    status:requests.Response=None
    json:dict=None
    w=None
    def __init__(self,auth,address):
        self.address=address
        self.auth=auth
        super(Sender,self).__init__()

    def run(self):
        print(self.json)
        try:
            self.status=requests.post("{address}/address/new".format(**dict(address=self.address)),auth=self.auth,json=self.json)
            print(self.status.status_code)
            self.w.statusBar().showMessage(str(self.status.status_code))
            time.sleep(3)
            self.w.statusBar().clearMessage()
            self.statusSig.emit(self.status)

        except Exception as e:
            self.w.statusBar().showMessage(str(e))
            time.sleep(3)
            self.w.statusBar().clearMessage()

