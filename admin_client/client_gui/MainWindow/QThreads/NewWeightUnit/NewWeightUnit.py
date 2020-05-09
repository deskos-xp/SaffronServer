import requests,sys,json,time
from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog

class NewWeightUnit(QThread):
    auth:tuple=None
    address:str=None
    w=None
    widget=None
    weightUnitSent=pyqtSignal(int)
    status:requests.Response=None
    json:dict=None
    def run(self):
        try:
            self.status=requests.post("{address}/weightUnit/new".format(**dict(address=self.address)),auth=self.auth,json=self.json)
            if self.status != None:
                self.w.statusBar().showMessage(str(self.status.status_code))
                self.weightUnitSent.emit(self.status.status_code)
        except Exception as e:
            print(e)
        self.finished.emit()
