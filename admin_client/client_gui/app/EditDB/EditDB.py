from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot,Qt
from PyQt5.QtWidgets import QDialog,QWidget,QStackedWidget,QTabWidget,QHeaderView
from PyQt5 import uic
import ast,os,sys,json
from .EditDBListModel import EditDBListModel
from .EditDBTableModel import EditDBTableModel
from .workers.priceUnitWorker import PriceUnitWorker
from .workers.weightUnitWorker import WeightUnitWorker
from .workers.SearchWorker import SearchWorker
from .EditDB_Controller_VBM import EditDB_Controller_VBM
from .EditDB_Controller_AD import EditDB_Controller_AD
from .EditDB_Controller_P import EditDB_Controller_P
from ..common.Fields import *

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
        self.selectedData=dict()
        self.editorControllers=dict()

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
            #build tabs 
            if wn in ['vendor','brand','manufacturer']:
                self.buildTabsVBM(wn)
            elif wn in ['address','department']:
                self.buildTabsAD(wn)
            elif wn in ['product']:
                self.buildTabsP(wn)

        self.dialog.exec_()
    def buildTabsVBM(self,wn):
        def wantsToSwitch(selectedData):
            wn='address'
            print(selectedData,"#"*30)
            self.selectedData[wn]=dict(selectedData)
            self.editorControllers[wn].data=selectedData
            self.editorControllers[wn].model.load_data(self.editorControllers[wn].data)
            self.editorControllers[wn].model.layoutChanged.emit()
            self.editorControllers[wn].old=dict(selectedData)
            w=getattr(self.dialog,wn)
            index=self.dialog.application.indexOf(w)
            self.dialog.application.setCurrentIndex(index)

        self.selectedData[wn]=dict()
        print("building tabs {wn}".format(**dict(wn=wn)))
        tab=getattr(self.dialog,wn)
        uic.loadUi("app/EditDB/forms/EditorVBM.ui",tab)
        self.editorControllers[wn]=EditDB_Controller_VBM(self.auth,self,tab,self.selectedData[wn],wn)
        self.editorControllers[wn].wantsToSwitch.connect(wantsToSwitch)

    def buildTabsAD(self,wn):
        self.selectedData[wn]=dict()
        tab=getattr(self.dialog,wn)
        uic.loadUi("app/EditDB/forms/EditorAD.ui",tab)
        self.editorControllers[wn]=EditDB_Controller_AD(self.auth,self,tab,self.selectedData[wn],wn)

    def buildTabsP(self,wn):
        self.selectedData[wn]=dict()
        tab=getattr(self.dialog,wn)
        uic.loadUi("app/EditDB/forms/EditorP.ui",tab)
        self.editorControllers[wn]=EditDB_Controller_P(self.auth,self,tab,self.selectedData[wn],wn)
        self.editorControllers[wn].wantsToSwitch.connect(self.fromProductTabTo)

    @pyqtSlot(dict)
    def fromProductTabTo(self,identifiers):
        print(identifiers)
        #get item from server
        def preUpdate(data):
            wn=identifiers.get("TYPE")
            self.selectedData[wn]=dict(data[0])
            self.editorControllers[wn].data=dict(data[0])
            self.editorControllers[wn].model.load_data(self.editorControllers[wn].data)
            self.editorControllers[wn].model.layoutChanged.emit()
            self.editorControllers[wn].old=dict(data[0])
            if wn not in ['product','department','address']:
                self.editorControllers[wn].setAddresses_address(self.editorControllers[wn].data.get("address"))
            index=self.dialog.application.indexOf(getattr(self.dialog,wn))
            self.dialog.application.setCurrentIndex(index)

        searchWorker=SearchWorker(self.auth,dict(page=0,limit=1,id=identifiers.get("ID")),identifiers.get("TYPE"),fields(identifiers.get("TYPE")))
        searchWorker.signals.hasError.connect(lambda e:print(e))
        #setValues in tab
        searchWorker.signals.hasItems.connect(preUpdate)
        QThreadPool.globalInstance().start(searchWorker)
        #set values in tab

        #switch to tab

    def buildGenericUi(self,wn):
        uic.loadUi("app/EditDB/forms/GenericWidget.ui",self.stackedWidgets[wn])
        self.stackedWidgets[wn].who.setText(wn[0].upper()+wn[1:])
        self.stackedWidgetsListModels[wn]=EditDBListModel()
        self.stackedWidgets[wn].results.setModel(self.stackedWidgetsListModels[wn]) 
        self.stackedWidgetsTableModels[wn]=EditDBTableModel(item={})
        self.stackedWidgets[wn].terms.setModel(self.stackedWidgetsTableModels[wn])
        self.stackedWidgets[wn].terms.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.stackedWidgets[wn].terms.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stackedWidgetsTableModels[wn].load_data(fields(wn))
        self.stackedWidgetsTableModels[wn].layoutChanged.emit()
        def SearchWorkerRun():
            clear()
            self.SearchWorkerRun(wn)
        def switchToTab(index):
            for i in range(self.dialog.application.count()):
                if self.dialog.application.tabText(i).lower() == wn:
                    self.dialog.application.setCurrentIndex(i)
                    selectedData=self.stackedWidgetsListModels[wn].items[index.row()]

                    ###
                    if wn not in ['product','department','address']:
                        self.selectedData[wn]=dict(selectedData)
                        self.editorControllers[wn].data=selectedData
                        self.editorControllers[wn].model.load_data(self.editorControllers[wn].data)
                        self.editorControllers[wn].model.layoutChanged.emit()
                        self.editorControllers[wn].old=dict(selectedData)
                        self.editorControllers[wn].setAddresses_address(selectedData.get('address'))
                    elif wn in ['address','department']:
                        print(selectedData,"#"*30)
                        self.selectedData[wn]=dict(selectedData)
                        self.editorControllers[wn].data=selectedData
                        self.editorControllers[wn].model.load_data(self.editorControllers[wn].data)
                        self.editorControllers[wn].model.layoutChanged.emit()
                        self.editorControllers[wn].old=dict(selectedData)
                    ###
                    print(selectedData,wn)

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


        def clearAll(state):
            clear(clearAll=True)


        def clear(clearAll=False):
            if clearAll == True:
                self.stackedWidgetsTableModels[wn].load_data(fields(wn))
                self.stackedWidgetsTableModels[wn].layoutChanged.emit()
            self.stackedWidgetsListModels[wn].items.clear()
            self.stackedWidgetsListModels[wn].layoutChanged.emit()

        self.stackedWidgets[wn].page.valueChanged.connect(onValueChanged)
        self.stackedWidgets[wn].limit.valueChanged.connect(onValueChanged)

        self.stackedWidgets[wn].search.clicked.connect(SearchWorkerRun)
        self.stackedWidgets[wn].back.clicked.connect(dec)
        self.stackedWidgets[wn].next.clicked.connect(inc)
        self.stackedWidgets[wn].clear.clicked.connect(clearAll)
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
        self.worker[wn]['search']=SearchWorker(self.auth,data,wn,fields(wn))
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
        self.stackedWidgetsTableModels[wn].load_data(fields(wn))
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
                    ###
                    #self.selectedData[wn]=selectedData
                    #print(selectedData,"#"*30)
                    self.selectedData[wn]=dict(selectedData)
                    self.editorControllers[wn].data=selectedData
                    self.editorControllers[wn].model.load_data(stripStructures(self.editorControllers[wn].data,delFields=["product_image","upc_image"]))
                    
                    self.editorControllers[wn].model.layoutChanged.emit()
                    self.editorControllers[wn].old=dict(selectedData)
                    
                    self.editorControllers[wn].setCombos_()
                    self.editorControllers[wn].getImages()
                    ###
                    #print(selectedData)

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
            self.stackedWidgetsTableModels[wn].load_data(fields(wn))
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


    def switch_stack(self,index):
        self.dialog.stackedWidget.setCurrentIndex(index.row())
