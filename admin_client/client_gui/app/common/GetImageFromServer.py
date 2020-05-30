from PyQt5.QtCore import QRunnable,QObject,QThreadPool,QThread,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap,QImage
import os,sys,json,ast,requests
from io import BytesIO

class GetImageFromServerSignals(QObject):
    kill:pyqtSignal=pyqtSignal()
    hasImage:pyqtSignal=pyqtSignal(QPixmap,str)
    hasBlankPixmap:pyqtSignal=pyqtSignal(QPixmap,str)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()
    session:requests.Session=requests.Session()

class GetImageFromServer(QRunnable):
    def __init__(self,auth:dict,productID:int,whichImage:str):
        self.auth=auth
        self.signals=GetImageFromServerSignals()
        self.whichImage=whichImage
        self.productID=productID
        self.address="{host}/product/get/{ID}/{WHICH}".format(**dict(host=self.auth.get("server_address"),ID=productID,WHICH=self.whichImage))
        print(self.address)
        super(GetImageFromServer,self).__init__()


    def run(self):
        print("starting ****")
        try:
            response=self.signals.session.get(
                    self.address,
                    auth=(
                        self.auth.get("username"),
                        self.auth.get("password")
                        ),
                    stream=True
                    )
            if response.status_code == 200:
                self.imgbio=BytesIO()
                for chunk in response.iter_content(1024):
                    self.imgbio.write(chunk)
                self.imgbio.seek(0)
                self.signals.hasImage.emit(QPixmap.fromImage(QImage.fromData(self.imgbio.read())),self.whichImage)
            else:
                self.signals.hasBlankPixmap.emit(QPixmap(),self.whichImage)
                raise Exception(str(response.status_code)+" id: {ID}".format(**dict(ID=self.productID)))
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
