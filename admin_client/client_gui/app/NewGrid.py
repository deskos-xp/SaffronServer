from PyQt5.QtWidgets import QMainWindow,QWidget
from PyQt5.QtCore import QCoreApplication,QThread,QThreadPool,pyqtSignal

import requests,json
import sys,time
from .QThreads.department import departmentThread
from .QThreads.vendor import vendorThread
from .QThreads.manufacturer import manufacturerThread
from .QThreads.brand import brandThread
from .QThreads.WeightUnit import WeightUnitThread           
from .QThreads.PriceUnit import PriceUnitThread
from .QThreads.Aquisition import aquisition
from .QThreads.ProductImgThread import getProductImages
from .QThreads.ProductImgUpdater import ProductImgUpdater
from .QThreads.ProductImgUpcUpdater import ProductUpcImgUpdater
from .QThreads.stylesheets import StyleSheet
from .QThreads.lock_counter_watcher import Watcher
class NewGrid(QWidget):
    address:str=None
    auth:tuple=None
    def result(self):
            im=self.sender()
            im.qthreaded.path=im.filename
            im.qthreaded.start()
            print(im.filename)


    def modWidgets(self):
        self.w.product_name.setStyleSheet(self.styleSheets.warning_LineEdit)
        self.w.product_name.textChanged.connect(self.product_name_check)
        
        self.w.homecode.setStyleSheet(self.styleSheets.warning_LineEdit)
        self.w.homecode.textChanged.connect(self.product_name_check)
        
        self.w.upc.setStyleSheet(self.styleSheets.warning_LineEdit)
        self.w.upc.textChanged.connect(self.product_name_check)

        self.w.case_count_sp.setStyleSheet(self.styleSheets.warning_SpinBox)
        self.w.case_count_sp.valueChanged.connect(self.spinbox_values) 

        self.w.weight_value.setStyleSheet(self.styleSheets.warning_SpinBox)
        self.w.weight_value.valueChanged.connect(self.spinbox_values)

        self.w.price_value.setStyleSheet(self.styleSheets.warning_SpinBox)
        self.w.price_value.valueChanged.connect(self.spinbox_values)

    def spinbox_values(self):
        p=self.sender()
        if p.value() <= 0:
            if p.objectName() in self.lock_counter_watcher.lock_counter.keys(): 
                self.lock_counter_watcher.lock_counter.__delitem__(p.objectName())
            p.setStyleSheet(self.styleSheets.warning_SpinBox)
        else:
            self.lock_counter_watcher.lock_counter[p.objectName()]=p
            p.setStyleSheet(self.styleSheets.default_SpinBox)

    def product_name_check(self):
        p=self.sender()
        
        if len(p.text()) <= 0:
            if p.objectName() in self.lock_counter_watcher.lock_counter.keys(): 
                self.lock_counter_watcher.lock_counter.__delitem__(p.objectName())
            p.setStyleSheet(self.styleSheets.warning_LineEdit)
        else:
            self.lock_counter_watcher.lock_counter[p.objectName()]=p
            p.setStyleSheet(self.styleSheets.default_LineEdit)

    def __init__(self,widget,auth,address):
        super(NewGrid,self).__init__() 
        self.address=address
        self.auth=auth
        self.lock_counter_watcher=Watcher(w=widget,TIME=0.25,unlock_len=6)
        self.lock_counter_watcher.parent=self
        self.lock_counter_watcher.start()
        self.w=widget
        self.styleSheets=StyleSheet()
        self.styleSheets.finished.connect(self.modWidgets)
        self.styleSheets.start()


        self.saving_progress=self.w.saving_progress
        
        self.saving_progress.hide()

        #self.auth=("admin","avalon")
        
        self.depThread=departmentThread()
        self.depThread.address=self.address
        self.depThread.w=widget
        self.depThread.auth=self.auth
        self.depThread.finished.connect(lambda :print(self.sender()))
        self.depThread.start()
        #'''
        self.vendThread=vendorThread()
        self.vendThread.address=self.address
        self.vendThread.w=widget
        self.vendThread.auth=self.auth
        self.vendThread.finished.connect(lambda :print(self.sender()))
        self.vendThread.start()
        #'''

        self.branThread=brandThread()
        self.branThread.address=self.address
        self.branThread.w=widget
        self.branThread.auth=self.auth
        self.branThread.finished.connect(lambda :print(self.sender()))
        self.branThread.start()
        #'''

        #'''
        self.manThread=manufacturerThread()
        self.manThread.address=self.address
        self.manThread.w=widget
        self.manThread.auth=self.auth
        self.manThread.finished.connect(lambda:print(self.sender()))
        self.manThread.start()
        #'''
        self.priceUnitThread=PriceUnitThread()
        self.priceUnitThread.address=self.address
        self.priceUnitThread.w=widget
        self.priceUnitThread.auth=self.auth
        self.priceUnitThread.finished.connect(lambda:print(self.sender()))
        self.priceUnitThread.start()

        self.weightUnitThread=WeightUnitThread()
        self.weightUnitThread.address=self.address
        self.weightUnitThread.w=widget
        self.weightUnitThread.auth=self.auth
        self.weightUnitThread.finished.connect(lambda:print(self.sender()))
        self.weightUnitThread.start()

        self.saveThread=aquisition()
        self.saveThread.address=self.address
        self.saveThread.auth=self.auth
        self.saveThread.w=widget
        self.saveThread.parent=self
        self.saveThread.finished.connect(lambda:print(self.sender()))
        
        widget.save_product_info.clicked.connect(self.saveThread.start)

        self.productImgUpdater=ProductImgUpdater()
        self.productImgUpdater.address=self.address
        self.productImgUpdater.auth=self.auth
        self.productImgUpdater.w=widget
        self.productImgUpdater.parent=self.parent

        self.productImg=getProductImages()
        self.productImg.w=widget
        self.productImg.qthreaded=self.productImgUpdater
        self.productImg.fname.connect(self.result)
        
        widget.browse_product_img_btn.clicked.connect(self.productImg.openFileNameDialog)

        self.productUpcImgUpdater=ProductUpcImgUpdater()
        self.productUpcImgUpdater.auth=self.auth
        self.productUpcImgUpdater.parent=self.parent
        self.productUpcImgUpdater.w=widget
        self.productUpcImgUpdater.address=self.address

        self.productUpc=getProductImages()
        self.productUpc.w=widget
        self.productUpc.qthreaded=self.productUpcImgUpdater

        self.productUpc.fname.connect(self.result)
        widget.browse_product_upc_img_btn.clicked.connect(self.productUpc.openFileNameDialog)
          
