from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
import requests,json,sys,time


class UpdateManufacturer(QThread):
    auth:tuple=None
    address:str=None
    w=None
    widget=None
    Updated=pyqtSignal(int)
    update_address:str=None
    def run(self):
        try:
            self.status=requests.get(self.update_address,auth=self.auth)
            if self.status != None:
                if self.status.json() != None:
                    self.Updated.emit(self.status.status_code)
        except Exception as e:
            print(e)
        self.finished.emit()
