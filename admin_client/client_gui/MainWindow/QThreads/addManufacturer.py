from PyQt5.QtCore import QThread,QCoreApplication
import requests,time

class AddExistingManufacturer(QThread):
    auth=None
    parent=None
    w=None
    address=None
    product_id=None

    def run(self):
        app=QCoreApplication.instance()
        self.addManufacturer() 
    def addManufacturer(self):
        manufacturers=self.parent.manThread.manufacturers
        while manufacturers == None:
            time.sleep(0.5)
            manufacturers=self.parent.manThread.manufacturers
            print("getting manufacturers : {}".format(manufacturers))
        selected=self.w.manufacturer_cb.currentText()
        manufacturerId=[i['id'] for i in manufacturers if i['name'] == selected]
        if not ((manufacturerId == []) or (manufacturerId == None)):
            manufacturerId=manufacturerId[0]
            response=requests.get("{}/product/update/{}/add/manufacturer/{}".format(self.address,self.product_id,manufacturerId),auth=self.auth)
