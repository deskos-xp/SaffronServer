from PyQt5.QtCore import QThread,QThreadPool,QObject,QRunnable,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog,QComboBox,QHeaderView

import os,sys,json,ast,requests
from ..common.Fields import *
from .EditDBTableModel import EditDBTableModel
from .workers.UpdateAD import UpdateAD

class EditDB_Controller_AD(QDialog):
    def update(self):
        self.parent.stackedWidgets[self.name].search.click()
        self.parent.updateAllCombos()

    def __init__(self,auth:dict,parent,tab,data:dict,name:str):
        super(EditDB_Controller_AD,self).__init__()
        self.auth=auth
        self.parent=parent
        self.tab=tab
        self.data=data
        self.old=dict(data)
        self.name=name
        self.model=EditDBTableModel(item=dict())
        self.tab.editor.setModel(self.model)
        self.tab.editor.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab.editor.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.buttons()

    def buttons(self):
        self.tab.reset.clicked.connect(self.resetTable)
        self.tab.save.clicked.connect(self.saveTableData)

    @pyqtSlot(bool)
    def resetTable(self,state):
        if not self.old:
            self.model.load_data(fields(self.name))
        else:
            self.model.load_data(self.old)
        self.model.layoutChanged.emit()

    def responded(self,response):
        if response.status_code == 200:
            self.update()
        print(response)

    @pyqtSlot(bool)
    def saveTableData(self,state):
        print(self.model.dataToItem())
        save=UpdateAD(self.auth,self.model.dataToItem(),self.model.dataToItem().get('id'),self.name)
        save.signals.hasError.connect(lambda x:print(x))
        save.signals.hasResponse.connect(self.responded)
        save.signals.disabledGrid.connect(self.tab.setEnabled)
        QThreadPool.globalInstance().start(save)

