from PyQt5.QtCore import QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog,QTableView,QComboBox,QPushButton,QHeaderView

import os,sys,json,ast,requests

from .EditDBTableModel import EditDBTableModel
from .EditDBTableModel import EditTableEnum
from .workers.SearchWorker import SearchWorker
from .workers.UpdateVBM import UpdateVBM

from ..common.Fields import *
class EditDB_Controller_VBM(QDialog):
    
    wantsToSwitch=pyqtSignal(dict)

    def update(self):
        self.parent.stackedWidgets[self.name].search.click()
        self.parent.updateAllCombos()

    def __init__(self,auth:dict,parent:QDialog,tab,data:dict,name:str):
        super(EditDB_Controller_VBM,self).__init__()
        self.auth=auth
        self.parent=parent
        self.data=data
        self.tab=tab
        self.name=name

        self.old=dict(data)

        self.model=EditDBTableModel(ID_MODE=EditTableEnum.NON_EDITABLE_ID)
        self.model.load_data(dict(data))
        self.model.layoutChanged.emit()
        self.tab.editor.setModel(self.model)
        self.tab.editor.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab.editor.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.buttons()
        self.load_addresses()
        self.setAddresses_address(data.get('address'))
        

    def setAddresses_address(self,data):
        if type(data) == type(list()):
            if len(data) > 0:
                data=data[0]
        print(data)
        if data in [None,[],{}]:
            self.tab.addresses.setCurrentIndex(-1)
        else:
            print("addresses count",self.tab.addresses.count())
            for i in range(self.tab.addresses.count()):
                ss=regexThisShit2(self.tab.addresses.itemText(i))
                if ss != None:
                    if int(ss.get('ID')) == data.get('id'):
                        print(ss,'*'*40)
                        self.tab.addresses.setCurrentIndex(i)
                        return
                        #break
                    else:
                        self.tab.addresses.setCurrentIndex(-1)
            else:
                self.tab.addresses.setCurrentIndex(-1)

    def load_addresses(self):
        def update_addresses(data):
            for d in data:
                string=toAddressString(d)
                contained=[self.tab.addresses.itemText(i) for i in range(self.tab.addresses.count())]
                if string not in contained:
                    self.tab.addresses.addItem(toAddressString(d))

        self.tab.addresses.lineEdit().setReadOnly(True)
        self.address_loader=SearchWorker(self.auth,dict(page=0,limit=sys.maxsize),'address',fields('address'))
        self.address_loader.signals.hasError.connect(lambda e:print(e))
        self.address_loader.signals.hasItems.connect(update_addresses)
        self.tab.addresses.clear()
        QThreadPool.globalInstance().start(self.address_loader)

    @pyqtSlot(bool)
    def save_data(self,state):
        self.tab.setEnabled(False)
        self.data=self.tab.editor.model().dataToItem()
        #worker thread needed to send updates
        self.POST=UpdateVBM(self.auth,self.data,regexThisShit2(self.tab.addresses.currentText()),self.name,Mode.POST)
        self.GET=UpdateVBM(self.auth,self.data,regexThisShit2(self.tab.addresses.currentText()),self.name,Mode.GET)
        
        self.GET.signals.disabledGrid.connect(self.tab.setEnabled)
        self.POST.signals.disabledGrid.connect(self.tab.setEnabled)

        self.POST.signals.hasError.connect(lambda e:print(e))
        self.GET.signals.hasError.connect(lambda e:print(e))

        self.POST.signals.hasResponse.connect(lambda e:print(e))
        self.GET.signals.hasResponse.connect(lambda e:print(e))

        self.POST.signals.finished.connect(self.update)
        self.GET.signals.finished.connect(self.update)

        QThreadPool.globalInstance().start(self.POST)
        QThreadPool.globalInstance().start(self.GET)
        self.tab.setEnabled(True)
        self.update()
        #send new data
        #remove address by id declared in old data
        #add new address by id declare in new data


    @pyqtSlot()
    def edit_address(self):
        wn=self.name
        def preSwitch(item):
            address=item
            if type(item) == type(list()):
                address=item[0]
            self.wantsToSwitch.emit(address)
            print(address)
            #self.parent.stackedWidgets

        address_data=regexThisShit2(self.tab.addresses.currentText())
        addrID=address_data.get('ID')
        searchL=SearchWorker(self.auth,dict(id=addrID,page=0,limit=sys.maxsize),'address',fields('address'))
        searchL.signals.hasError.connect(lambda x:print(x))
        searchL.signals.hasItem.connect(preSwitch)
        searchL.signals.hasItems.connect(preSwitch)

        QThreadPool.globalInstance().start(searchL)
        print(address_data)

    def buttons(self):
        self.tab.save.clicked.connect(self.save_data)
        self.tab.reset.clicked.connect(self.resetTable)
        self.tab.edit_address.clicked.connect(self.edit_address)

    @pyqtSlot(bool)
    def resetTable(self,state):
        print(id(self.old),id(self.data))
        self.model.load_data(dict(self.old))
        self.model.layoutChanged.emit()
        if type(self.old.get('address')) == type(list()):
            self.setAddresses_address(dict(self.old.get('address')[0]))
        elif type(self.old.get('address')) == type(dict()):
            self.setAddresses_address(dict(self.old.get('address')))
