from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot,Qt
from PyQt5.QtWidgets import QDialog,QWidget,QStackedWidget,QTabWidget,QHeaderView
from PyQt5 import uic
import ast,os,sys,json
from .EditDBListModel import EditDBListModel
from .EditDBTableModel import EditDBTableModel
from .workers.priceUnitWorker import PriceUnitWorker
from .workers.weightUnitWorker import WeightUnitWorker
from .workers.SearchWorker import SearchWorker

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
        #QDialog.u
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
                self.buildGenericUi(wn=wn)
            else:
                self.buildProductUi(wn=wn)
                self.productWorkersBasic()
                self.productWorkersComplex()

        self.dialog.exec_()
    def buildGenericUi(self,wn):
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
        def SearchWorkerRun():
            clear()
            self.SearchWorkerRun(wn)

        def switchToTab(index):
            for i in range(self.dialog.application.count()):
                if self.dialog.application.tabText(i).lower() == wn:
                    self.dialog.application.setCurrentIndex(i)
                    selectedData=self.stackedWidgetsListModels[wn].items[index.row()]
                    print(selectedData)

        def inc(state):
            self.stackedWidgets[wn].page.setValue(self.stackedWidgets[wn].page.value()+1)
            #self.SearchWorkerRun(wn)

        def dec(state):
            self.stackedWidgets[wn].page.setValue(self.stackedWidgets[wn].page.value()-1)
            #self.SearchWorkerRun(wn)
        
        
        def onValueChanged(state):
            if self.sender().objectName() == "page":
                if self.sender().value() < 1:
                    self.sender().setValue(0)
                    self.stackedWidgets[wn].back.setEnabled(False)
                else:
                    self.stackedWidgets[wn].back.setEnabled(True)
            self.SearchWorkerRun(wn)

        def clear():
            self.stackedWidgetsTableModels[wn].load_data(self.fields(wn))
            self.stackedWidgetsTableModels[wn].layoutChanged.emit()
            self.stackedWidgetsListModels[wn].items.clear()
            self.stackedWidgetsListModels[wn].layoutChanged.emit()

        self.stackedWidgets[wn].page.valueChanged.connect(onValueChanged)
        self.stackedWidgets[wn].limit.valueChanged.connect(onValueChanged)

        self.stackedWidgets[wn].search.clicked.connect(SearchWorkerRun)
        self.stackedWidgets[wn].back.clicked.connect(dec)
        self.stackedWidgets[wn].next.clicked.connect(inc)
        self.stackedWidgets[wn].clear.clicked.connect(clear)
        self.stackedWidgets[wn].results.activated.connect(switchToTab)

    def SearchWorkerRun(self,wn,preSearch=None):
        def updateModel(data):
            self.stackedWidgetsListModels[wn].items.clear()
            self.stackedWidgetsListModels[wn].layoutChanged.emit()
            print(data,"tag"*4)
            if data in [[],{},None] or type(data) == type(Exception()):
                self.stackedWidgets[wn].next.setEnabled(False)
                if self.stackedWidgets[wn].page.value() >= 1:
                    self.stackedWidgets[wn].page.setValue(self.stackedWidgets[wn].page.value()-1)
                if type(data) == type(Exception()):
                    return
            else:
                self.stackedWidgets[wn].next.setEnabled(True)
            if type(data) == type(dict()):
                self.stackedWidgetsListModels[wn].items.append(data)
                self.stackedWidgetsListModels[wn].layoutChanged.emit()
            elif type(data) == type(list()):
                for d in data:
                    self.stackedWidgetsListModels[wn].items.append(d)
                    self.stackedWidgetsListModels[wn].layoutChanged.emit()

        if self.worker.get(wn) == None:
            self.worker[wn]=dict()
        data=self.stackedWidgetsTableModels[wn].dataToItem()
        data['page']=self.stackedWidgets[wn].page.value()
        data['limit']=self.stackedWidgets[wn].limit.value()
        if preSearch != None:
            data=preSearch(data)
        self.worker[wn]['search']=SearchWorker(self.auth,data,wn,self.fields(wn))
        self.worker[wn]['search'].signals.hasError.connect(updateModel)
        self.worker[wn]['search'].signals.hasItem.connect(updateModel)
        self.worker[wn]['search'].signals.hasItems.connect(updateModel)
        self.worker[wn]['search'].signals.finished.connect(lambda : print("search finished!"))

        QThreadPool.globalInstance().start(self.worker[wn]['search'])


    def buildProductUi(self,wn):
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


        def stateOfInclusion(state):
            #print(state)
            toChange=self.sender().objectName().replace("use","")
            if toChange.lower() == "casecount":
                toChange=toChange.lower()
            else:
                toChange=toChange[0].lower()+toChange[1:]
            getattr(self.stackedWidgets[wn],toChange).setEnabled(state)

        def SearchWorkerRun():
            clear()
            self.SearchWorkerRun(wn,preSearch=preSearch)

        def switchToTab(index):
            for i in range(self.dialog.application.count()):
                if self.dialog.application.tabText(i).lower() == wn:
                    self.dialog.application.setCurrentIndex(i)
                    selectedData=dict(self.stackedWidgetsListModels[wn].items[index.row()])
                    print(selectedData)

        def preSearch(searchAbleData): 
            if self.stackedWidgets[wn].weight.isEnabled():
                res=self.stackedWidgets[wn].weight.value()
                if res.is_integer():
                    res=int(res)
                searchAbleData['weight']=res
            if self.stackedWidgets[wn].price.isEnabled():
                res=self.stackedWidgets[wn].price.value()
                if res.is_integer():
                    res=int(res)
                searchAbleData['price']=res
            if self.stackedWidgets[wn].weightUnit.isEnabled():
                searchAbleData['weightUnit']=self.stackedWidgets[wn].weightUnit.currentText()
            if self.stackedWidgets[wn].priceUnit.isEnabled():
                searchAbleData['priceUnit']=self.stackedWidgets[wn].priceUnit.currentText()
            print(searchAbleData)
            if self.stackedWidgets[wn].casecount.isEnabled():
                searchAbleData['case_count']=self.stackedWidgets[wn].casecount.value()

            return searchAbleData 

        def inc(state):
            self.stackedWidgets[wn].page.setValue(self.stackedWidgets[wn].page.value()+1)
            #self.SearchWorkerRun(wn)

        def dec(state):
            self.stackedWidgets[wn].page.setValue(self.stackedWidgets[wn].page.value()-1)
            #self.SearchWorkerRun(wn)
        
        
        def onValueChanged(state):
            if self.sender().objectName() == "page":
                if self.sender().value() < 1:
                    self.sender().setValue(0)
                    self.stackedWidgets[wn].back.setEnabled(False)
                else:
                    self.stackedWidgets[wn].back.setEnabled(True)
            SearchWorkerRun()

        def clear():
            self.stackedWidgetsTableModels[wn].load_data(self.fields(wn))
            self.stackedWidgetsTableModels[wn].layoutChanged.emit()
            self.stackedWidgetsListModels[wn].items.clear()
            self.stackedWidgetsListModels[wn].layoutChanged.emit()

        self.stackedWidgets[wn].page.valueChanged.connect(onValueChanged)
        self.stackedWidgets[wn].limit.valueChanged.connect(onValueChanged)

        self.stackedWidgets[wn].search.clicked.connect(SearchWorkerRun)
        self.stackedWidgets[wn].back.clicked.connect(dec)
        self.stackedWidgets[wn].next.clicked.connect(inc)
        self.stackedWidgets[wn].clear.clicked.connect(clear)
        self.stackedWidgets[wn].results.activated.connect(switchToTab)

        self.stackedWidgets[wn].usePriceUnit.toggled.connect(stateOfInclusion)
        self.stackedWidgets[wn].usePrice.toggled.connect(stateOfInclusion)
        self.stackedWidgets[wn].useWeightUnit.toggled.connect(stateOfInclusion)
        self.stackedWidgets[wn].useWeight.toggled.connect(stateOfInclusion)
        self.stackedWidgets[wn].useCaseCount.toggled.connect(stateOfInclusion)


    def productWorkersComplex(self,re=False,wn='product'):
        pass
        #i now need a searchWorker that is generic enough to be used for all entities

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
