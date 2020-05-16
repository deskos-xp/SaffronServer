from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QObject,QRunnable,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QComboBox

import json,ast,os
from dotenv import load_dotenv
from .workers.priceUnitWorker import PriceUnitWorker
from .workers.weightUnitWorker import WeightUnitWorker
from .workers.GenericWorker import Worker
from .workers.NewProductWorker import NewProductWorker
from .workers.NewProductUpdateWorker import NewProductUpdateWorker

class NewProduct(QWidget):
    def __init__(self,auth:dict,widget:QWidget):
        super(NewProduct,self).__init__()
        print(auth)
        self.auth=auth
        self.widget=widget
        self.qtp=QThreadPool.globalInstance()

        uic.loadUi("app/NewProduct/forms/NewProduct.ui",self.widget)
        
        self.priceUnitWorker=PriceUnitWorker()
        self.priceUnitWorker.signals.hasUnit.connect(widget.priceUnit.addItem)
        self.qtp.start(self.priceUnitWorker)

        self.weightUnitWorker=WeightUnitWorker()
        self.weightUnitWorker.signals.hasUnit.connect(widget.weightUnit.addItem)
        self.qtp.start(self.weightUnitWorker)

        self.manufacturerWorker=Worker(auth,"manufacturer",self.widget.manufacturer)
        self.manufacturerWorker.signals.hasItem.connect(self.addToCombo)
        self.qtp.start(self.manufacturerWorker)

        self.brandWorker=Worker(auth,"brand",self.widget.brand)
        self.brandWorker.signals.hasItem.connect(self.addToCombo)
        self.qtp.start(self.brandWorker)

        self.vendorWorker=Worker(auth,"vendor",self.widget.vendor)
        self.vendorWorker.signals.hasItem.connect(self.addToCombo)
        self.qtp.start(self.vendorWorker)

        self.departmentWorker=Worker(auth,"department",self.widget.department)
        self.departmentWorker.signals.hasItem.connect(self.addToCombo)
        self.qtp.start(self.departmentWorker)

        self.widget.save.clicked.connect(self.construct_and_send) 

    def construct_and_send(self):
        newProductData=self.constructNewProductData()
        #make new product worker
        response=NewProductWorker(self.auth,newProductData)
        response.signals.hasProductId.connect(self.updateProduct)
        #response.signals.hasResponse.connect(lambda x:print(x))
        self.qtp.start(response)
        
    def updateProduct(self,product_id):
        manufacturer_uri=self.constructUpdateAdd(self.widget.manufacturer,"product",product_id)
        m_worker=NewProductUpdateWorker(self.auth,manufacturer_uri)
        m_worker.signals.hasError.connect(self.errorHandler)
        m_worker.signals.finished.connect(self.status)

        vendor_uri=self.constructUpdateAdd(self.widget.vendor,"product",product_id)
        v_worker=NewProductUpdateWorker(self.auth,vendor_uri)
        v_worker.signals.hasError.connect(self.errorHandler)
        v_worker.signals.finished.connect(self.status)

        brand_uri=self.constructUpdateAdd(self.widget.brand,"product",product_id)
        b_worker=NewProductUpdateWorker(self.auth,brand_uri)
        b_worker.signals.hasError.connect(self.errorHandler)
        b_worker.signals.finished.connect(self.status)

        department_uri=self.constructUpdateAdd(self.widget.department,"product",product_id)
        d_worker=NewProductUpdateWorker(self.auth,department_uri)
        d_worker.signals.hasError.connect(self.errorHandler)
        d_worker.signals.finished.connect(self.status)

        #upload images

        self.qtp.start(d_worker)
        self.qtp.start(b_worker)
        self.qtp.start(v_worker)
        self.qtp.start(m_worker)

        print(department_uri,brand_uri,vendor_uri,manufacturer_uri,sep="\n")
        
    def status(self):
        print(self.sender().objectName(),"stage completed!")

    def errorHandler(self,error):
        print(error)

    def constructUpdateAdd(self,combobox,WHAT,product_id) -> str:
        text=combobox.currentText()
        ID=text.split("-")[0]
        url="{address}/{WHAT}/update/{product_id}/add/{WHO}/{ID}".format(address=self.auth.get("server_address"),WHAT=WHAT,ID=ID,product_id=product_id,WHO=combobox.objectName())
        return url

    def constructNewProductData(self) -> dict:
        payload=dict(
            upc=self.widget.upc.text(),
            home_code=self.widget.homecode.text(),
            name=self.widget.name.text(),
            case_count=self.widget.casecount.value(),
            comment=self.widget.comment.toPlainText(),
            priceUnit=self.widget.priceUnit.currentText(),
            price=self.widget.price.value(),
            weightUnit=self.widget.weightUnit.currentText(),
            weight=self.widget.weight.value()
        )
        return payload

    def addToCombo(self,combo,data):
        print(data,combo)
        combo.addItem("{id} - {name}".format(**data))
