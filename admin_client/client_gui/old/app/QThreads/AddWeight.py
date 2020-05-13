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
from .AddPricing import AddPrice

class AddWeight(QThread):
    w=None
    auth=None
    #address="http://localhost:9000"
    address=None
    parent=None
    product_id=None

    def run(self):
        app=QCoreApplication.instance();
        self.product_weight_handler(self.product_id)        
    
    def product_weight_handler(self,product_id):
        weight_id=self.add_weight(product_id)
        self.add_weight_to_product(weight_id,product_id)

 
    def add_weight(self,product_id):
        value=self.w.weight_value.value()
        response=requests.post("{}/weight/new".format(self.address),json=dict(value=value),auth=self.auth)
        weightId=None
        if 'id' in response.json().keys():
            weightId=response.json()['id']
        else:
            pass
        units=self.parent.weightUnitThread.weight_units
        while units == None:
            time.sleep(0.5)
            print("getting weight units: {}".format(units))
            units=self.parent.weightUnitThread.weight_units
        print(self.w.weight_unit.currentText())
        print([i['name'] for i in units])
        weightUnitID=[i['id'] for i in units if i['name'] == str(self.w.weight_unit.currentText())]
        if len(weightUnitID) > 0:
            weightUnitID=weightUnitID[0]
        print(weightUnitID)
        if not ((weightUnitID == []) or (weightUnitID == None)):
            response=requests.get("{}/weight/update/{}/add/{}".format(self.address,weightId,weightUnitID),auth=self.auth)
            #if 'id' in response.json().keys():
        return weightId
        
    def add_weight_to_product(self,weight_id,product_id):
        response=requests.get("{}/product/update/{}/add/weight/{}".format(self.address,product_id,weight_id),auth=self.auth)


