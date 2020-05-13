from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
import json,requests,sys

class NewManufacturer(QThread):
    manufacturerSent:pyqtSignal=pyqtSignal(int)
    address:str=None
    auth:tuple=None
    widget=None
    w=None
    json:dict=None
    def run(self):
        status=requests.post("{address}/manufacturer/new".format(**dict(address=self.address)),auth=self.auth,json=self.json)
        print(status)
        try:
            j=status.json()
            if j == None:
                self.finished.emit()
                return
            manufacturerID=j.get("id")
            if manufacturerID == None:
                self.finished.emit()
                return

            self.manufacturerSent.emit(manufacturerID)
            self.finished.emit()
        except Exception as e:
            print(e)
