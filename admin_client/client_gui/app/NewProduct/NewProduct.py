from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QObject,QRunnable,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QComboBox,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QProgressBar,QComboBox

import json,ast,os
from dotenv import load_dotenv
from .workers.priceUnitWorker import PriceUnitWorker
from .workers.weightUnitWorker import WeightUnitWorker
from .workers.GenericWorker import Worker
from .workers.NewProductWorker import NewProductWorker
from .workers.NewProductUpdateWorker import NewProductUpdateWorker
from .workers.UploaderWorker import UploaderWorker
class NewProduct(QWidget):
    def __init__(self,auth:dict,widget:QWidget):
        super(NewProduct,self).__init__()
        print(auth)
        self.auth=auth
        self.widget=widget
        self.qtp=QThreadPool.globalInstance()
        
        self.upc_img=None
        self.product_img=None

        uic.loadUi("app/NewProduct/forms/NewProduct.ui",self.widget)
        
        self.initialize()        

        self.widget.nav_product_img.clicked.connect(self.getProductImg)
        self.widget.nav_upc_img.clicked.connect(self.getUPCImg)

        self.widget.save.clicked.connect(self.construct_and_send)
        
        self.widget.progressBar.hide()

        self.widget.product_img_path.textChanged.connect(self.tryPath)
        self.widget.upc_img_path.textChanged.connect(self.tryPath)

    def initialize(self,re=False):
        if re == True:
            self.widget.vendor.clear()
            self.widget.manufacturer.clear()
            self.widget.brand.clear()
            self.widget.department.clear()
            
        self.priceUnitWorker=PriceUnitWorker()
        self.priceUnitWorker.signals.hasUnit.connect(self.widget.priceUnit.addItem)
        self.qtp.start(self.priceUnitWorker)

        self.weightUnitWorker=WeightUnitWorker()
        self.weightUnitWorker.signals.hasUnit.connect(self.widget.weightUnit.addItem)
        self.qtp.start(self.weightUnitWorker)

        self.manufacturerWorker=Worker(self.auth,"manufacturer",self.widget.manufacturer)
        self.manufacturerWorker.signals.hasItem.connect(self.addToCombo)
        self.qtp.start(self.manufacturerWorker)

        self.brandWorker=Worker(self.auth,"brand",self.widget.brand)
        self.brandWorker.signals.hasItem.connect(self.addToCombo)
        self.qtp.start(self.brandWorker)

        self.vendorWorker=Worker(self.auth,"vendor",self.widget.vendor)
        self.vendorWorker.signals.hasItem.connect(self.addToCombo)
        self.qtp.start(self.vendorWorker)

        self.departmentWorker=Worker(self.auth,"department",self.widget.department)
        self.departmentWorker.signals.hasItem.connect(self.addToCombo)
        self.qtp.start(self.departmentWorker)

    def tryPath(self,text):
        pixmap=None
        if os.path.exists(text) and os.path.isfile(text):
            print("file exists... attempting to load it as an img")
            if self.sender().objectName() == "product_img_path":
                pixmap=self.pathToQPixmap(text)
                self.widget.product_img.setPixmap(pixmap)
                if pixmap != None:
                   self.product_img=text 
            elif self.sender().objectName() == "upc_img_path":
                pixmap=self.pathToQPixmap(text)
                self.widget.upc_img.setPixmap(pixmap)
                if pixmap != None:
                    self.upc_img=text
        else:
            if self.sender().objectName() == "product_img_path":
                self.product_img=None
            elif self.sender().objectName() == "upc_img_path":
                self.upc_img=None

    def getFilePathDialog(self,caption,) -> str:
            fname = QFileDialog.getOpenFileName(self.widget, caption,'.',"Image files (*.jpg *.gif *.png)") 
            if fname: 
                return fname[0]

    def getProductImg(self):
        path=self.getFilePathDialog("Open Product Image...")
        self.widget.product_img_path.setText(path)
        
    def pathToQPixmap(self,path) -> QPixmap:
        try:
            return QPixmap(path)
        except Exception as e:
            print(e)
            return None

    def getUPCImg(self):
        path=self.getFilePathDialog("Open UPC Image...")
        self.widget.upc_img_path.setText(path)

    def construct_and_send(self):
        self.widget.progressBar.show()

        self.widget.progressBar.setMaximum(0)
        self.widget.progressBar.setMaximum(self.widget.progressBar.maximum()+1)
        newProductData=self.constructNewProductData()
        #make new product worker
        response=NewProductWorker(self.auth,newProductData)
        response.signals.hasProductId.connect(self.updateProduct)
        response.signals.finished.connect(self.status)
        #response.signals.hasResponse.connect(lambda x:print(x))
        self.qtp.start(response)
        
    def updateProduct(self,product_id):
        self.widget.progressBar.setMaximum(self.widget.progressBar.maximum()+1)
        manufacturer_uri=self.constructUpdateAdd(self.widget.manufacturer,"product",product_id)
        m_worker=NewProductUpdateWorker(self.auth,manufacturer_uri)
        m_worker.signals.hasError.connect(self.errorHandler)
        m_worker.signals.finished.connect(self.status)

        self.widget.progressBar.setMaximum(self.widget.progressBar.maximum()+1)
        vendor_uri=self.constructUpdateAdd(self.widget.vendor,"product",product_id)
        v_worker=NewProductUpdateWorker(self.auth,vendor_uri)
        v_worker.signals.hasError.connect(self.errorHandler)
        v_worker.signals.finished.connect(self.status)

        self.widget.progressBar.setMaximum(self.widget.progressBar.maximum()+1)
        brand_uri=self.constructUpdateAdd(self.widget.brand,"product",product_id)
        b_worker=NewProductUpdateWorker(self.auth,brand_uri)
        b_worker.signals.hasError.connect(self.errorHandler)
        b_worker.signals.finished.connect(self.status)

        self.widget.progressBar.setMaximum(self.widget.progressBar.maximum()+1)
        department_uri=self.constructUpdateAdd(self.widget.department,"product",product_id)
        d_worker=NewProductUpdateWorker(self.auth,department_uri)
        d_worker.signals.hasError.connect(self.errorHandler)
        d_worker.signals.finished.connect(self.status)

        #upload images
        if self.product_img != None:
            self.widget.progressBar.setMaximum(self.widget.progressBar.maximum()+1)
            product_img_worker=UploaderWorker(self.auth,"product_image",self.product_img,product_id)
            product_img_worker.signals.uploaded.connect(self.status) 
            product_img_worker.signals.finished.connect(self.status)

            self.qtp.start(product_img_worker)

        if self.upc_img != None:
            self.widget.progressBar.setMaximum(self.widget.progressBar.maximum()+1)
            upc_img_worker=UploaderWorker(self.auth,"upc_image",self.upc_img,product_id)
            upc_img_worker.signals.uploaded.connect(self.status) 
            upc_img_worker.signals.finished.connect(self.status)

            self.qtp.start(upc_img_worker)


        self.qtp.start(d_worker)
        self.qtp.start(b_worker)
        self.qtp.start(v_worker)
        self.qtp.start(m_worker)

        print(department_uri,brand_uri,vendor_uri,manufacturer_uri,sep="\n")
        
    def status(self,response,WHAT):
        print(response,WHAT)

    def status(self):
        self.widget.progressBar.setValue(self.widget.progressBar.value()+1)
        if self.widget.progressBar.value() >= self.widget.progressBar.maximum():
            self.widget.progressBar.hide()
        print(self.sender(),"stage completed!")

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

    def addToCombo(self,combo:QComboBox,data):
        print(data,combo)
        item="{id} - {name}".format(**data)
        #QComboBox.itemText
        items=[combo.itemText(i) for i in range(combo.count())]
        if item not in items:
            combo.addItem(item)
