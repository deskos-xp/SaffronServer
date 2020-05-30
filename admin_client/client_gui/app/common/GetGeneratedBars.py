from PyQt5.QtCore import QObject,QRunnable,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage,QPixmap
from io import BytesIO
import os,sys,json,ast,requests

class GetGeneratedUPCSignals(QObject):
    killMe:bool=False
    hasImage:pyqtSignal=pyqtSignal(QPixmap,str)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()
    session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class GetGeneratedUPC(QRunnable):
    def __init__(self,auth:dict,productID:int,TYPE="ean13",WHO=None):
        super(GetGeneratedUPC,self).__init__()
        self.auth=auth
        self.productID=productID
        self.signals=GetGeneratedUPCSignals()
        self.TYPE=TYPE
        self.WHO=WHO


    def run(self):
        try:
            addr= "{server_address}/product/barcode/{ID}/{TYPE}".format(**dict(server_address=self.auth.get("server_address"),ID=self.productID,TYPE=self.TYPE))
            print(addr)
            response=self.signals.session.get(
                    addr,
                    stream=True,
                    auth=(self.auth.get("username"),self.auth.get("password"))
                    )
            print(response)
            if response.status_code == 200:
                self.imgbio=BytesIO()
                for chunk in response.iter_content(1024):
                    self.imgbio.write(chunk)
                self.imgbio.seek(0)
                pixmap=QPixmap.fromImage(QImage.fromData(self.imgbio.read()))
                self.signals.hasImage.emit(pixmap,self.WHO)
            else:
                raise Exception(str(response.status_code))
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
