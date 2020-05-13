from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog,QWidget
from PyQt5.QtGui import QPixmap,QImage

from .GetProductImg import GetProductImg
from .GetGeneratedUPC import GetGeneratedUPC
class DisplayDataDialog:
    data=None
    auth=None
    address=None
    w=None
    widget=None
    def processImg(self,img,Type):
        im=QImage.fromData(img.read())
        if Type == "upc_image":
            self.widget.upc_image.setPixmap(QPixmap.fromImage(im))
        elif Type == "product_image":
            self.widget.product_image.setPixmap(QPixmap.fromImage(im))
        elif Type == "barcode":
            self.widget.generated_upc.setPixmap(QPixmap.fromImage(im))
        else:
            raise BaseException("not a valid image type")

    def run(self):
        #handle imgs
        self.widget=QDialog(self.w)
        uic.loadUi("app/forms/DisplayProductDataDialog.ui",self.widget)
        self.widget.close.rejected.connect(self.widget.reject)
        self.widget.name.setText(self.data.get("name"))
        self.widget.upc.setText(self.data.get("upc"))
        self.widget.homecode.setText(self.data.get("home_code"))
        self.widget.ID.setValue(self.data.get("id"))

        self.upcImg=GetProductImg()
        self.upcImg.w=self.w
        self.upcImg.auth=self.auth
        self.upcImg.address=self.address
        self.upcImg.img_type="upc_image"
        self.upcImg.recieved.connect(self.processImg)
        self.upcImg.productID=self.data.get("id")
        self.upcImg.start()

        self.productImg=GetProductImg()
        self.productImg.w=self.w
        self.productImg.auth=self.auth
        self.productImg.address=self.address
        self.productImg.img_type="product_image"
        self.productImg.recieved.connect(self.processImg)
        self.productImg.productID=self.data.get("id")
        self.productImg.start()
        #get generated barcode
        self.generatedUPCThread=GetGeneratedUPC(self.w,self.auth,self.address,self.data.get("id"))
        self.generatedUPCThread.recieved.connect(self.processImg)
        self.generatedUPCThread.start()

        if self.data.get("case_count") == None:
            self.data['case_count']=0
        self.widget.case_count.setValue(self.data.get("case_count"))

        self.departmentDialog=DisplayGeneralView(ui="department")
        self.departmentDialog.data=self.data.get("departments")
        if self.departmentDialog.data != None:
            self.departmentDialog.w=self.w
            self.widget.department_btn.clicked.connect(self.departmentDialog.run)
 
        self.manufacturerDialog=DisplayGeneralView(ui="manufacturer")
        self.manufacturerDialog.data=self.data.get("manufacturers")
        if self.manufacturerDialog.data != None:
            self.manufacturerDialog.w=self.w
            self.widget.manufacturer_btn.clicked.connect(self.manufacturerDialog.run)
 
        self.brandDialog=DisplayGeneralView(ui="brand")
        self.brandDialog.data=self.data.get("brands")
        if self.brandDialog.data != None:
            self.brandDialog.w=self.w
            self.widget.brand_btn.clicked.connect(self.brandDialog.run)
        
        self.vendorDialog=DisplayGeneralView(ui="vendor")
        self.vendorDialog.data=self.data.get("vendors")
        if self.vendorDialog.data != None:
            self.vendorDialog.w=self.w
            self.widget.vendor_btn.clicked.connect(self.vendorDialog.run)
        self.widget.comment.setText(self.data.get("comment"))
        self.widget.exec_()
        print(self.data)
        
class DisplayItem:
    w=None
    data=None
    widget=None
    ui=""
    addressDialog=None
    def show_Address(self):
        self.addressDialog=QDialog(self.widget)
        uic.loadUi("app/forms/AddressView.ui",self.addressDialog)
        address=self.data.get("address")
        if address != None:
            address=address[0]
            if address != {}:
                self.addressDialog.street_number.setText(address.get("street_number"))
                self.addressDialog.street_name.setText(address.get("street_name"))
                self.addressDialog.city.setText(address.get("city"))
                self.addressDialog.state.setText(address.get("state"))
                self.addressDialog.ZIP.setText(address.get("ZIP"))
                self.addressDialog.apartment.setText(address.get("apartment_suite"))

        self.addressDialog.confirm.rejected.connect(self.addressDialog.reject)
        self.addressDialog.show()

    def run(self):
        self.widget=QWidget(self.w)
        if self.ui == "department":
            uic.loadUi("app/forms/DepartmentView.ui",self.widget)
            self.widget.name.setText(self.data.get("name"))
            self.widget.store_department_number.setValue(self.data.get("store_department_number"))
            self.widget.ID.setValue(self.data.get("id"))
            self.widget.comment.setText(self.data.get("comment"))
        else:
            uic.loadUi("app/forms/GeneralViewDialog.ui",self.widget)    
            self.widget.name.setText(self.data.get("name"))
            self.widget.email.setText(self.data.get("email"))
            self.widget.phone.setText(self.data.get("phone"))
            self.widget.comment.setText(self.data.get("comment"))
            self.widget.ID.setValue(self.data.get("id"))
            self.widget.address_btn.clicked.connect(self.show_Address)

            #self.widget.address_btn.clicked.connect()
               

class DisplayGeneralView:
    data=None
    #auth=None
    #address=None
    w=None
    widget=None
    displays=[]
    ui=""
    def __init__(self,ui=""):
        self.ui=ui
    def run(self):
        self.widget=QDialog(self.w)
        uic.loadUi("app/forms/ContainerGrid.ui",self.widget)
        for num,unit in enumerate(self.data):
            tmp=DisplayItem()
            tmp.ui=self.ui
            tmp.data=unit
            tmp.w=self.w
            tmp.run()
            
            self.displays.append(tmp)
            self.widget.item_grid.addWidget(tmp.widget,num,0,0,0)
        self.widget.close.rejected.connect(self.widget.reject)
        self.widget.exec_()
             
