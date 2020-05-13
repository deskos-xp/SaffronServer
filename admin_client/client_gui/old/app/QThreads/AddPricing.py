from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QCoreApplication,QThread,QThreadPool,pyqtSignal

import requests,json
import sys,time
from .department import departmentThread
from .vendor import vendorThread
from .manufacturer import manufacturerThread
from .brand import brandThread
from .WeightUnit import WeightUnitThread           
from .PriceUnit import PriceUnitThread

class AddPrice(QThread):
    auth=None
    parent=None
    w=None
    product_id=None
    address=None
    def run(self):
        self.product_price_handler(self.product_id)

    def product_price_handler(self,product_id):
        price_id=self.add_price(product_id)
        self.add_price_to_product(price_id,product_id)

    def add_price(self,product_id):
        value=self.w.price_value.value()
        priceId=None
        response=requests.post("{}/price/new".format(self.address),json=dict(value=value),auth=self.auth)
        if 'id' in response.json().keys():
            priceId=response.json()['id']
        units=self.parent.priceUnitThread.price_units
        while units == None:
            time.sleep(0.5)
            print("getting price units: {}".format(units))
            units=self.parent.priceUnitThread.price_units
        
        print(self.w.price_unit.currentText())
        print([i['name'] for i in units])
        priceUnitID=[i['id'] for i in units if i['name'] == str(self.w.price_unit.currentText())]
        
        if len(priceUnitID) > 0:
            priceUnitID=priceUnitID[0]
        print(priceUnitID)
        if not (priceUnitID == [] or priceUnitID == None):
            response=requests.get("{}/price/update/{}/add/{}".format(self.address,priceId,priceUnitID),auth=self.auth)
            print(response.json())
            #if 'id' in response.json().keys():
        return priceId

    def add_price_to_product(self,price_id,product_id):
        print(self.auth)
        response=requests.get("{}/product/update/{}/add/price/{}".format(self.address,product_id,price_id),auth=self.auth)
        print(product_id,price_id)
        print(response)



