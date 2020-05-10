from PyQt5.QtCore import QThread,QCoreApplication
import requests,time

class AddExistingBrand(QThread):
    auth=None
    parent=None
    w=None
    address=None
    product_id=None

    def run(self):
        app=QCoreApplication.instance()
        self.addBrand()
    
    def addBrand(self):
        brands=self.parent.branThread.brands
        while brands == None:
            time.sleep(0.5)
            brands=self.parent.branThread.brands
            print("getting brands : {}".format(brands))
        selected=self.w.brand_cb.currentText()
        brandId=[i['id'] for i in brands if i['name'] == selected]
        if not ((brandId == []) or (brandId == None)):
            brandId=brandId[0]
            response=requests.get("{}/product/update/{}/add/brand/{}".format(self.address,self.product_id,brandId),auth=self.auth)
