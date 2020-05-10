from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
import json,requests,sys

class NewBrand(QThread):
    brandSent:pyqtSignal=pyqtSignal(int)
    address:str=None
    auth:tuple=None
    widget=None
    w=None
    json:dict=None
    def run(self):
        status=requests.post("{address}/brand/new".format(**dict(address=self.address)),auth=self.auth,json=self.json)
        print(status)
        try:
            j=status.json()
            if j == None:
                self.finished.emit()
                return
            brandID=j.get("id")
            if brandID == None:
                self.finished.emit()
                return

            self.brandSent.emit(brandID)
            self.finished.emit()
        except Exception as e:
            print(e)
