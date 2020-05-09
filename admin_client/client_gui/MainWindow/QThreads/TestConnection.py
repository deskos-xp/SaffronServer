from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
import requests,time,sys

class Check(QThread):
    widget=None
    auth=None
    address=None
    status:pyqtSignal=pyqtSignal(int)
    def run(self):
        try:
            self.address=self.widget.address.text()
            self.auth=tuple([self.widget.username.text(),self.widget.password.text()])

            self.response=requests.get("{address}/user/get/1".format(**dict(address=self.address)),auth=self.auth)
            self.status.emit(self.response.status_code)
            self.widget.root.statusBar().showMessage(str(self.response.status_code))
            time.sleep(5)
            self.widget.root.statusBar().clearMessage()
        except Exception as e:
            print(e)
            self.status.emit(-1)
            self.widget.root.statusBar().showMessage(str(e))
            time.sleep(5)
            self.widget.root.statusBar().clearMessage()

