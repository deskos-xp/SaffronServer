from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QAction,QWidget,QDialog
from PyQt5 import uic
from .QThreads.NewAddress.NewAddressController import NewAddressController
from .QThreads.NewBrand.NewBrandDialogController import NewBrandDialogController
from .QThreads.NewVendor.NewVendorDialogController import NewVendorDialogController
from .QThreads.NewManufacturer.NewManufacturerDialogController import NewManufacturerDialogController
from .QThreads.NewDepartment.NewDepartmentDialogController import NewDepartmentDialogController
from .QThreads.NewPriceUnit.NewPriceUnitDialogController import NewPriceUnitDialogController
from .QThreads.NewWeightUnit.NewWeightUnitDialogController import NewWeightUnitDialogController
class MenuBar:
    w=None
    bar=None
    def init_action_exit(self):
        self.exitButton=QAction(QIcon("MainWindow/Icons/exit24.png"),'Exit',self.w)
        self.exitButton.setShortcut('Ctrl+E')
        self.exitButton.setStatusTip('Exit application')
        self.exitButton.triggered.connect(self.w.close)
        self.filemenu.addAction(self.exitButton)


    def view_about(self):
        self.aboutDialog.exec_()

    def init_about_dialog(self):
        aboutDialog=QDialog(self.w)
        uic.loadUi("MainWindow/forms/About.ui",aboutDialog)
        aboutDialog.close.rejected.connect(aboutDialog.reject)
        aboutDialog.program_img.setPixmap(QPixmap("MainWindow/Icons/SaffronExplorer.png"))
        aboutDialog.setWindowTitle("About")
        self.aboutDialog=aboutDialog
                #self.aboutDialog.reject)
        #modify viewable data here

    def init_action_about(self):
        self.about_action=QAction(QIcon("MainWindow/Icons/about.png"),"About",self.w)
        self.about_action.setStatusTip("About the program")
        self.about_action.triggered.connect(self.view_about)
        self.helpmenu.addAction(self.about_action)

    def add_new_department(self):
        self.new_department_dialog=QDialog(self.w)
        uic.loadUi("MainWindow/forms/NewDepartment.ui",self.new_department_dialog)
        self.new_department_dialog_controller=NewDepartmentDialogController(self.new_department_dialog,self.w,self.w.address,self.w.auth)
        #self.new_department_dialog_controller.auth=self.w.auth
        #self.new_department_dialog_controller.w=self.w
        #self.new_department_dialog_controller.widget=self.new_department_dialog
        self.new_department_dialog.show()

    def add_new_address(self):
        self.new_address_dialog=QDialog(self.w)
        uic.loadUi("MainWindow/forms/NewAddress.ui",self.new_address_dialog)
        self.new_address_dialog_controller=NewAddressController(self.new_address_dialog)
        self.new_address_dialog_controller.auth=self.w.auth
        self.new_address_dialog_controller.address=self.w.address
        self.new_address_dialog_controller.w=self.w
        #self.new_address_dialog_controller.widget=self.new_address_dialog
        self.new_address_dialog.show()


    def add_new_brand(self):
        self.new_brand_dialog=QDialog(self.w)
        uic.loadUi("MainWindow/forms/NewEntityGeneral.ui",self.new_brand_dialog)
        self.new_brand_dialog_controller=NewBrandDialogController(self.new_brand_dialog,self.w.address,self.w.auth)
        self.new_brand_dialog_controller.w=self.w
        #self.new_brand_dialog_controller.widget=self.w
        #self.new_brand_dialog_controller.auth=self.w.auth
        #self.new_brand_dialog_controller.address=self.w.address
        self.new_brand_dialog.show()

    def add_new_priceUnit(self):
        self.new_priceUnit_dialog=QDialog(self.w)
        uic.loadUi("MainWindow/forms/NewUnit.ui",self.new_priceUnit_dialog)
        self.new_priceUnit_dialog_controller=NewPriceUnitDialogController(self.new_priceUnit_dialog,self.w,self.w.address,self.w.auth)
        self.new_priceUnit_dialog.show()

    def add_new_weightUnit(self):
        self.new_weightUnit_dialog=QDialog(self.w)
        uic.loadUi("MainWindow/forms/NewUnit.ui",self.new_weightUnit_dialog)
        self.new_weightUnit_dialog_controller=NewWeightUnitDialogController(self.new_weightUnit_dialog,self.w,self.w.address,self.w.auth)
        self.new_weightUnit_dialog.show()

    def add_new_vendor(self):
        self.new_vendor_dialog=QDialog(self.w)
        uic.loadUi("MainWindow/forms/NewEntityGeneral.ui",self.new_vendor_dialog)
        print(self.w.address)
        self.new_vendor_dialog_controller=NewVendorDialogController(self.new_vendor_dialog,self.w.address,self.w.auth)
        self.new_vendor_dialog_controller.w=self.w
        self.new_vendor_dialog.show()

    def add_new_manufacturer(self):
        self.new_manufacturer_dialog=QDialog(self.w)
        uic.loadUi("MainWindow/forms/NewEntityGeneral.ui",self.new_manufacturer_dialog)
        print(self.w.address)
        self.new_manufacturer_dialog_controller=NewManufacturerDialogController(self.new_manufacturer_dialog,self.w.address,self.w.auth)
        self.new_manufacturer_dialog_controller.w=self.w
        self.new_manufacturer_dialog.show()

    def init_action_new_department(self):
        self.new_department=QAction(QIcon("MainWindow/Icons/new_department.png"),"&Department",self.w)
        self.new_department.setStatusTip("Add a new department")
        self.new_department.triggered.connect(self.add_new_department)
        self.newmenu.addAction(self.new_department)

    def init_action_new_address(self):
        self.new_address=QAction(QIcon("MainWindow/Icons/new_address.png"),"&Address",self.w)
        self.new_address.setStatusTip("Add a new address")
        self.new_address.triggered.connect(self.add_new_address)
        self.newmenu.addAction(self.new_address)

    def init_action_new_manufacturer(self):
        self.new_manufacturer=QAction(QIcon("MainWindow/Icons/new_manufacturer.png"),"&Manufacturer",self.w)
        self.new_manufacturer.setStatusTip("Add New Manufacturer")
        self.new_manufacturer.triggered.connect(self.add_new_manufacturer)
        self.newmenu.addAction(self.new_manufacturer)

    def init_action_new_vendor(self):
        self.new_vendor=QAction(QIcon("MainWindow/Icons/new_vendor.png"),"&Vendor",self.w)
        self.new_vendor.setStatusTip("Add New Vendor")
        self.new_vendor.triggered.connect(self.add_new_vendor)
        self.newmenu.addAction(self.new_vendor)

    def init_action_new_weightUnit(self):
        self.new_weightUnit=QAction(QIcon("MainWindow/Icons/new_weightUnit.png"),"&Weight Unit",self.w)
        self.new_weightUnit.setStatusTip("Add a new Weight Unit")
        self.new_weightUnit.triggered.connect(self.add_new_weightUnit)
        self.newmenu.addAction(self.new_weightUnit)

    def init_action_new_priceUnit(self):
        self.new_priceUnit=QAction(QIcon("MainWindow/Icons/new_priceUnit.png"),"&Price Unit",self.w)
        self.new_priceUnit.setStatusTip("Add a new Price Unit")
        self.new_priceUnit.triggered.connect(self.add_new_priceUnit)
        self.newmenu.addAction(self.new_priceUnit)

    def init_action_new_brand(self):
        self.new_brand=QAction(QIcon("MainWindow/Icons/new_brand.png"),"&Brand",self.w)
        self.new_brand.setStatusTip("Add a new Brand")
        self.new_brand.triggered.connect(self.add_new_brand)
        self.newmenu.addAction(self.new_brand)

    def init_action_new_dialogs(self):
        self.init_action_new_address()
        self.init_action_new_brand()
        self.init_action_new_vendor()
        self.init_action_new_manufacturer()
        self.init_action_new_department()
        self.init_action_new_priceUnit()
        self.init_action_new_weightUnit()

    def init_menus(self):
        self.filemenu=self.bar.addMenu("&File")
        self.newmenu=self.bar.addMenu("&New")
        self.helpmenu=self.bar.addMenu("&Help")

    def __init__(self,w):
        self.w=w
        self.bar=self.w.menuBar()
        self.init_menus()
        self.init_action_exit()
        self.init_about_dialog()
        self.init_action_about()
        self.init_action_new_dialogs()
           
    #adding base entities will be initiated from here via dialogs
