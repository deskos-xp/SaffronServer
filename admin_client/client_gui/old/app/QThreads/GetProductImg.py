from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
import time,sys,requests
from io import BytesIO
class GetProductImg(QThread):
    w=None
    auth:tuple=None
    address:str=None
    response:requests.Response=None
    productID:int=None
    img_type:str=None
    imgbio:BytesIO=None
    recieved:pyqtSignal=pyqtSignal(BytesIO,str)
    def run(self):
        print(self)
        self.response=requests.get("{address}/product/get/{id}/{img_type}".format(**dict(address=self.address,id=self.productID,img_type=self.img_type)),auth=self.auth,stream=True)
        if self.response.status_code == 200:
            self.imgbio=BytesIO()
            for chunk in self.response.iter_content(1024):
                self.imgbio.write(chunk)
            self.imgbio.seek(0)
            self.recieved.emit(self.imgbio,self.img_type)
        print(self.response.reason)
