from PyQt5.QtCore import QCoreApplication,QObject,QRunnable,QThreadPool,pyqtSignal,pyqtSlot,Qt
from PyQt5.QtWidgets import QDialog,QWidget,QHeaderView
from PyQt5 import uic

import os,sys,json,ast

from .DataViewSmallModel import DataViewSmallModel
from .DataViewSmallListModel import DataViewSmallListModel

class DataViewSmall(QDialog):
    def __init__(self,auth:dict,data:list,widget:QWidget):
        self.auth=auth
        self.data=data
        self.widget=widget
        super(DataViewSmall,self).__init__()

        self.modelList=DataViewSmallListModel()
        self.modelList.items=data
        
        
        self.model=DataViewSmallModel(auth=self.auth)
        
        self.dialog=QDialog(widget)
        uic.loadUi("app/DataViewSmall/forms/DataViewSmall.ui",self.dialog)
        

        self.dialog.listView.setModel(self.modelList)
        self.dialog.listView.activated.connect(self.viewData)
        self.dialog.dataView.setModel(self.model)

        self.addressViewModel=DataViewSmallModel()
        self.dialog.addressView.setModel(self.addressViewModel)


        print(data,"*"*44) 
        
        self.model.layoutChanged.emit()
        self.dialog.exec_()

    def viewData(self,index):
        print(index.row(),self.modelList.items)
        self.model.load_data(self.modelList.items[index.row()])

        self.dialog.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dialog.dataView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.model.layoutChanged.emit()
        address=self.modelList.items[index.row()].get("address")
        if address != None:
            try:
                self.addressViewModel.load_data(address[0])
                self.dialog.addressView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.dialog.addressView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.addressViewModel.layoutChanged.emit()
            except Exception as e:
                print(e)

        self.dialog.tabWidget.setCurrentIndex(1)
        '''
            if address in data show button to display address
            on button_address clicked switch to address tab to display address info
        '''
