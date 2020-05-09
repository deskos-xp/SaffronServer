from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
import json,requests,sys

class NewVendor(QThread):
    vendorSent:pyqtSignal=pyqtSignal(int)
    address:str=None
    auth:tuple=None
    widget=None
    w=None
    json:dict=None
    def run(self):
        status=requests.post("{address}/vendor/new".format(**dict(address=self.address)),auth=self.auth,json=self.json)
        print(status)
        try:
            j=status.json()
            if j == None:
                self.finished.emit()
                return
            vendorID=j.get("id")
            if vendorID == None:
                self.finished.emit()
                return

            self.vendorSent.emit(vendorID)
            self.finished.emit()
        except Exception as e:
            print(e)
