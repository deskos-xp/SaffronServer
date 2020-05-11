from PyQt5 import uic
from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal,QObject,QThreadPool,QModelIndex

from PyQt5.QtWidgets import QDialog,QComboBox,QWidget,QListWidgetItem,QListWidget,QStackedWidget
import ast,json,sys,os,requests
from .widgets.UpdateSelector import UpdateSelector 
from PyQt5.QtGui import QStandardItemModel
from .StackChanger import StackChanger
from .widgets.EntityStackModule.EntityStack import EntityStack

class DeleteDialog(QDialog,StackChanger):
    auth:tuple=None
    address:str=None
    w:QWidget=None
    dialog:QDialog=None
    def __init__(self,parent:QWidget,address:str,auth:tuple):
        super(DeleteDialog,self).__init__()

        self.auth=auth
        self.address=address
        self.w=parent
        self.dialog=QDialog(parent)
        uic.loadUi("app/DeleteDialog/forms/DeleteDialog.ui",self.dialog)

        self.qtp=QThreadPool.globalInstance()
        updaterSelector=UpdateSelector(self.w,self.dialog.selector)
        updaterSelector.signals.ready.connect(self.selector_ud)

        self.qtp.start(updaterSelector)        
        self.dialog.selector.activated.connect(self.stack_changer)
        
        #widget
        self.adr=EntityStack(self.w,self.dialog.address,self.dialog,self.address,self.auth,"address")
        self.adr.done_del.connect(self.progress_statement) 
        #for first displayable widget that user will see so selector is populated
        self.adr.worker.signals.waitResult=False
        self.enabledWidgetsChanger.append(self.adrCH)


        self.brand=EntityStack(self.w,self.dialog.brand,self.dialog,self.address,self.auth,"brand")
        self.brand.done_del.connect(self.progress_statement)
        self.enabledWidgetsChanger.append(self.brandCH)

        self.vendor=EntityStack(self.w,self.dialog.vendor,self.dialog,self.address,self.auth,"vendor")
        self.vendor.done_del.connect(self.progress_statement)               
        self.enabledWidgetsChanger.append(self.vendorCH)

        self.manufacturer=EntityStack(self.w,self.dialog.manufacturer,self.dialog,self.address,self.auth,"manufacturer")
        self.manufacturer.done_del.connect(self.progress_statement)               
        self.enabledWidgetsChanger.append(self.manufacturerCH)

        self.department=EntityStack(self.w,self.dialog.department,self.dialog,self.address,self.auth,"department")
        self.department.done_del.connect(self.progress_statement)               
        self.enabledWidgetsChanger.append(self.departmentCH)

        self.priceUnit=EntityStack(self.w,self.dialog.priceUnit,self.dialog,self.address,self.auth,"priceUnit")
        self.priceUnit.done_del.connect(self.progress_statement)               
        self.enabledWidgetsChanger.append(self.priceUnitCH)

        self.weightUnit=EntityStack(self.w,self.dialog.weightUnit,self.dialog,self.address,self.auth,"weightUnit")
        self.weightUnit.done_del.connect(self.progress_statement)               
        self.enabledWidgetsChanger.append(self.weightUnitCH)

        self.product=EntityStack(self.w,self.dialog.product,self.dialog,self.address,self.auth,"product")
        self.product.done_del.connect(self.progress_statement)               
        self.enabledWidgetsChanger.append(self.productCH)






        self.dialog.show() 

    def progress_statement(self):
        print("Done Deleting Object")
        self.w.sb.showMessage("Done Deleting Object!",10)

        #QListWidget.

    def selector_ud(self,model):
        for i in model:
            self.dialog.selector.addItem(QListWidgetItem(i))


