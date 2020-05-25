from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot,Qt
from PyQt5.QtWidgets import QDialog,QWidget,QStackedWidget,QTabWidget,QHeaderView
from PyQt5 import uic
import ast,os,sys,json
from .EditDBListModel import EditDBListModel
from .EditDBTableModel import EditDBTableModel
from .workers.priceUnitWorker import PriceUnitWorker
from .workers.weightUnitWorker import WeightUnitWorker


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
        
        self.worker=dict()

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
            else:
                uic.loadUi("app/EditDB/forms/GenericWidgetProduct.ui",self.stackedWidgets[wn])
                self.stackedWidgetsListModels[wn]=EditDBListModel()
                self.stackedWidgets[wn].results.setModel(self.stackedWidgetsListModels[wn])
                self.stackedWidgetsTableModels[wn]=EditDBTableModel(item={})
                self.stackedWidgets[wn].terms.setModel(self.stackedWidgetsTableModels[wn])
                self.stackedWidgets[wn].terms.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.stackedWidgets[wn].terms.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.stackedWidgetsTableModels[wn].load_data(self.fields(wn))
                self.stackedWidgetsTableModels[wn].layoutChanged.emit()
                self.stackedWidgets[wn].who.setText(wn[0].upper()+wn[1:])
                self.worker[wn]=dict()
                self.productWorkersBasic()

        self.dialog.exec_()
    def productWorkersBasic(self,re=False,wn='product'):
        def updatePriceUnit(data):
            print(data)
            #if data not in widget
            self.stackedWidgets[wn].priceUnit.addItem(data)

        def updateWeightUnit(data):
            self.stackedWidgets[wn].weightUnit.addItem(data)
            print(data)

        def reset():
            self.stackedWidgets[wn].weightUnit.clear()
            self.stackedWidgets[wn].priceUnit.clear()

        if re == True:
            reset()

        #from PyQt5.QtWidgets import QComboBox
        #QComboBox.lineEdit.setAlignment(Qt.AlignCenter)
        self.stackedWidgets[wn].weightUnit.lineEdit().setAlignment(Qt.AlignCenter)
        self.stackedWidgets[wn].priceUnit.lineEdit().setAlignment(Qt.AlignCenter)
        self.stackedWidgets[wn].priceUnit.lineEdit().setReadOnly(True)
        self.stackedWidgets[wn].weightUnit.lineEdit().setReadOnly(True)

        self.worker[wn]['price']=PriceUnitWorker()
        self.worker[wn]['price'].signals.hasUnit.connect(updatePriceUnit)
        self.worker[wn]['price'].signals.hasError.connect(lambda x:print(x))

        self.worker[wn]['weight']=WeightUnitWorker()
        self.worker[wn]['weight'].signals.hasUnit.connect(updateWeightUnit)
        self.worker[wn]['weight'].signals.hasError.connect(lambda x:print(x))

        for k in self.worker[wn].keys():
            QThreadPool.globalInstance().start(self.worker[wn][k])



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
