from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QObject,QRunnable,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QComboBox

import json,ast,os
from dotenv import load_dotenv
from .workers.priceUnitWorker import PriceUnitWorker
from .workers.weightUnitWorker import WeightUnitWorker
from .workers.GenericWorker import Worker
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

    def addToCombo(self,combo,data):
        print(data,combo)
        combo.addItem("{id} - {name}".format(**data))
