from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal

import requests,time,sys,os
from PyQt5.QtWidgets import QLabel,QWidget
from io import BytesIO
class GetGeneratedUPC(QThread):
    w=None
    widget=None
    auth:tuple=None
    address:str=None
    productID:int=None
    barcode_gen_address:str=None
    recieved:pyqtSignal=pyqtSignal(BytesIO,str)
    response:requests.Response=None
    imgbio:BytesIO=None

    def __init__(self,parent,auth:tuple,address:str,productID:int) -> None:
        self.w=parent
        self.address=address
        self.auth=auth
        self.productID=productID
        self.imgbio=BytesIO()
        self.barcode_gen_address="{address}/product/barcode/{ID}/{TYPE}".format(**dict(address=address,ID=productID,TYPE="ean13"))
        super(GetGeneratedUPC,self).__init__()

    def run(self):
        self.response=requests.get(self.barcode_gen_address,auth=self.auth,stream=True)
        if self.response.status_code == 200:
            self.imgbio=BytesIO()
            for chunk in self.response.iter_content(1024):
                self.imgbio.write(chunk)
            self.imgbio.seek(0)
            self.recieved.emit(self.imgbio,"barcode")
        print(self.response.reason)

        self.finished.emit()
