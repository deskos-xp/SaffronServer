from PyQt5.QtCore import QThread,QCoreApplication
import requests,time

class AddExistingVendor(QThread):
    auth=None
    parent=None
    w=None
    address=None
    product_id=None

    def run(self):
        app=QCoreApplication.instance()
        self.addVendor() 
    def addVendor(self):
        vendors=self.parent.vendThread.vendors
        while vendors == None:
            time.sleep(0.5)
            vendors=self.parent.vendThread.vendors
            print("getting vendors : {}".format(vendors))
        selected=self.w.vendor_cb.currentText()
        vendorId=[i['id'] for i in vendors if i['name'] == selected]
        if not ((vendorId == []) or (vendorId == None)):
            vendorId=vendorId[0]
            response=requests.get("{}/product/update/{}/add/vendor/{}".format(self.address,self.product_id,vendorId),auth=self.auth)
