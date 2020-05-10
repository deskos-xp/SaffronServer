import requests,sys,time
from PyQt5.QtCore import QCoreApplication,QThread,pyqtSignal
from PyQt5.QtWidgets import QLabel

class Uploader(QThread):
    address=None
    parent=None
    auth=None
    w=None
    upload_type=('upc_image','product_image')
    product_id=None
    msg="file could not be uploaded as it does not exist!"
    upc_uploaded=pyqtSignal(requests.Response,str)
    product_img_uploaded=pyqtSignal(requests.Response,str)

    def run(self):
        app=QCoreApplication.instance()
        self.upload_product_img()
        self.upload_product_upc_img()

    def upload_product_upc_img(self):
        try:
            print("uploading product upc img...")
            with open(self.w.product_upc_img_lbl.text(),"rb") as fd:
                files={
                    "file":fd
                        }

                response=requests.post(
                        "{}/product/update/{}/upload/upc_image".format(self.address,self.product_id),
                        json=dict(),
                        auth=self.auth,
                        files=files
                        )
                self.upc_uploaded.emit(response,"upc_image")
            
        except FileNotFoundError as e:
            print(e)
            print(self.msg)

    def upload_product_img(self):
        try:
            print("uploading product img...")
            with open(self.w.product_img_lbl.text(),"rb") as fd:
                files={
                    "file":fd
                    }

                response=requests.post(
                        "{}/product/update/{}/upload/product_image".format(self.address,self.product_id),
                        json=dict(),
                        auth=self.auth,
                        files=files
                        )
                self.product_img_uploaded.emit(response,"product_image")
        except FileNotFoundError as e:
            print(e)
            print(self.msg)
