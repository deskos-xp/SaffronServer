from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QObject,QRunnable,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QComboBox

import json,ast,os
from dotenv import load_dotenv
from .workers.priceUnitWorker import PriceUnitWorker
from .workers.weightUnitWorker import WeightUnitWorker
class NewProduct(QWidget):
    def __init__(self,auth:dict,widget:QWidget):
        super(NewProduct,self).__init__()
        print(auth)
        self.auth=auth
        self=widget
        self.qtp=QThreadPool.globalInstance()

        uic.loadUi("app/NewProduct/forms/NewProduct.ui",self)
        
        self.priceUnitWorker=PriceUnitWorker()
        self.priceUnitWorker.signals.hasUnit.connect(widget.priceUnit.addItem)
        self.qtp.start(self.priceUnitWorker)

        self.weightUnitWorker=WeightUnitWorker()
        self.weightUnitWorker.signals.hasUnit.connect(widget.weightUnit.addItem)
        self.qtp.start(self.weightUnitWorker)

