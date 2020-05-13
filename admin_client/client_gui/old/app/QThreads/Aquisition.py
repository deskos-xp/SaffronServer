from PyQt5.QtWidgets import QMainWindow,QProgressBar
from PyQt5.QtCore import QCoreApplication,QThread,QThreadPool,pyqtSignal

import requests,json
import sys,time
from .department import departmentThread
from .vendor import vendorThread
from .manufacturer import manufacturerThread
from .brand import brandThread
from .WeightUnit import WeightUnitThread           
from .PriceUnit import PriceUnitThread

from .AddPricing import AddPrice
from .AddWeight import AddWeight
from .addDepartment import AddExistingDepartment
from .addVendor import AddExistingVendor
from .addBrand import AddExistingBrand
from .addManufacturer import AddExistingManufacturer
from .Uploader import Uploader

class aquisition(QThread):
    w=None
    auth=None
    address=None
    parent=None

    def run(self):
        app=QCoreApplication.instance();
        self.mkProduct_commit(self.mkProduct_json())

    def mkProduct_json(self) -> dict:
        name=self.w.product_name.text()
        homecode=self.w.homecode.text()
        upc=self.w.upc.text()
        comment=self.w.product_comment.toPlainText()
        case_count=self.w.case_count_sp.value()
        product=dict(name=name,home_code=homecode,upc=upc,comment=comment,case_count=case_count)
        return product


    counter=0
    total_stages=7
    def progress(self):
        pbar:QProgressBar=self.w.saving_progress
        if pbar.isHidden() == True:
            pbar.show()
        self.counter+=1
        print("{}/{} - {}".format(self.counter,self.total_stages,self.sender()))
        if pbar.value() < self.total_stages:
            pbar.setValue(self.counter)
        if pbar.value() == self.total_stages:
            pbar.setValue(0)
            pbar.hide()
            self.counter=0

    def mkProduct_commit(self,json:dict):
        try:
            #make new base product from json:dict
            response=requests.post("{}/product/new".format(self.address),json=json,auth=self.auth)
            try:
                if 'id' in response.json().keys():
                    pass
            except Exception as e:
                print(e)
                return
            print(response) 
            if 'id' in response.json().keys():
                product_id=response.json()['id']
                #add price
                self.priceAddThread=AddPrice()
                self.priceAddThread.auth=self.auth
                self.priceAddThread.w=self.w
                self.priceAddThread.product_id=product_id
                self.priceAddThread.parent=self.parent
                self.priceAddThread.address=self.address
                self.priceAddThread.finished.connect(self.progress)
                self.priceAddThread.start()
                #add weight
                self.weightAddThread=AddWeight()
                self.weightAddThread.auth=self.auth
                self.weightAddThread.w=self.w
                self.weightAddThread.product_id=product_id
                self.weightAddThread.parent=self.parent
                self.weightAddThread.address=self.address
                self.weightAddThread.finished.connect(self.progress)
                self.weightAddThread.start()
                self.departmentThread=AddExistingDepartment()           
                self.departmentThread.auth=self.auth
                self.departmentThread.w=self.w
                self.departmentThread.product_id=product_id
                self.departmentThread.address=self.address
                self.departmentThread.parent=self.parent
                self.departmentThread.finished.connect(self.progress)
                self.departmentThread.start()
                self.vendorThread=AddExistingVendor()           
                self.vendorThread.auth=self.auth
                self.vendorThread.w=self.w
                self.vendorThread.product_id=product_id
                self.vendorThread.parent=self.parent
                self.vendorThread.address=self.address
                self.vendorThread.finished.connect(self.progress)
                self.vendorThread.start()
                self.brandThread=AddExistingBrand()           
                self.brandThread.auth=self.auth
                self.brandThread.w=self.w
                self.brandThread.product_id=product_id
                self.brandThread.address=self.address
                self.brandThread.parent=self.parent
                self.brandThread.finished.connect(self.progress)
                self.brandThread.start()
                self.manufacturerThread=AddExistingManufacturer()           
                self.manufacturerThread.auth=self.auth
                self.manufacturerThread.w=self.w
                self.manufacturerThread.product_id=product_id
                self.manufacturerThread.parent=self.parent
                self.manufacturerThread.address=self.address
                self.manufacturerThread.finished.connect(self.progress)
                self.manufacturerThread.start()
                
                self.productImgUploader=Uploader()
                self.productImgUploader.auth=self.auth
                self.productImgUploader.address=self.address
                self.productImgUploader.parent=self.parent
                self.productImgUploader.w=self.w
                self.productImgUploader.product_id=product_id
                self.productImgUploader.finished.connect(self.progress)
                self.productImgUploader.start()
                self.productImgUploader.upc_uploaded.connect(self.uploads)
                self.productImgUploader.product_img_uploaded.connect(self.uploads)
        except Exception as e:
            print(e)
            self.w.statusBar().showMessage("there was an error!")
    def uploads(self,response,TYPE):
        print(response,TYPE)
