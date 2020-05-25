from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget,QStackedWidget,QTabWidget,QHeaderView
from PyQt5 import uic
import ast,os,sys,json
from .EditDBListModel import EditDBListModel
from .EditDBTableModel import EditDBTableModel

class EditDB(QDialog):
    def __init__(self,auth:dict,parent):
        self.auth=auth
        self.parent=parent
        super(EditDB,self).__init__()
        self.dialog=QDialog()
        uic.loadUi("app/EditDB/forms/EditDB_dialog.ui",self.dialog)

        widgetNames=(
            "address",
            "vendor",
            "brand",
            "manufacturer",
            "department",
            "product"
                )

        self.searchModel=EditDBListModel(items=widgetNames)
        self.dialog.listView.setModel(self.searchModel)
        self.dialog.listView.activated.connect(self.switch_stack)
        
        self.stackedWidgetsListModels=dict()
        self.stackedWidgetsTableModels=dict()

        self.stackedWidgets=dict()
        for wn in widgetNames:
            self.stackedWidgets[wn]=QWidget()
            self.dialog.stackedWidget.addWidget(self.stackedWidgets[wn])
            self.dialog.stackedWidget.setCurrentIndex(0)
            if wn not in ['product']:
                uic.loadUi("app/EditDB/forms/GenericWidget.ui",self.stackedWidgets[wn])
                self.stackedWidgets[wn].who.setText(wn[0].upper()+wn[1:])
                self.stackedWidgetsListModels[wn]=EditDBListModel()
                self.stackedWidgets[wn].results.setModel(self.stackedWidgetsListModels[wn])
                
                self.stackedWidgetsTableModels[wn]=EditDBTableModel(item={})
                self.stackedWidgets[wn].terms.setModel(self.stackedWidgetsTableModels[wn])
                self.stackedWidgets[wn].terms.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.stackedWidgets[wn].terms.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.stackedWidgetsTableModels[wn].load_data(self.fields(wn))
                self.stackedWidgetsTableModels[wn].layoutChanged.emit()


        self.dialog.exec_()

    def fields(self,name):
        def addressFields():
            return dict(
                    city="",
                    state="",
                    street_number="",
                    street_name="",
                    ZIP="",
                    apartment_suite=""
                    )
        def genericFields():
            return dict(
                comment="",
                name="",
                email="",
                phone=""
                    )
        def departmentFields():
            return dict(
                comment="",
                name="",
                store_department_number=0
                    )
        def productFields():
            return dict(
                    comment="",
                    upc="",
                    homecode="",
                    priceUnit="",
                    weightUnit=""
                    )


        if name == 'address':
            return addressFields()
        elif name in ['vendor','manufacturer','brand']:
            return genericFields()
        elif name == 'department':
            return departmentFields()
        elif name == 'product':
            return productFields()
        else:
            return dict()


    def switch_stack(self,index):
        self.dialog.stackedWidget.setCurrentIndex(index.row())
