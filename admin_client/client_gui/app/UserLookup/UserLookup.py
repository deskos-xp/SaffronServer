from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json,ast,requests
from ..common.TableModel import TableModel
from ..common.editable_table_model import editable_table_model as ETM
from ..common.ModelDelegates import *
from ..common.Fields import * 
from ..common.ListModel import ListModel
from ..common.SetupModelView import setupViews

class UserLookup(QDialog):
    def __init__(self,auth:dict,parent:QWidget):
        super(UserLookup,self).__init__()
        self.auth=auth
        self.parent=parent
        self.dialog=QDialog()
        uic.loadUi("app/UserLookup/forms/UserLookup.ui",self.dialog)
        
        self.searchModel=ETM(item=fields("user")) 
        self.resultModel=ListModel(items=[])
        self.dialog.resultsView.setModel(self.resultModel)

        self.userModel=TableModel(item=fields("user"))
                
        self.prep_delegates(self.dialog.searchView)        
        setupViews(self,viewsList=['searchView','userView'],modelsList=['searchModel','userModel'])

        self.dialog.search_button.clicked.connect(self.search)
        self.dialog.clear.clicked.connect(self.clearFields)
        self.dialog.page.setValue(0)
        self.dialog.limit.setValue(15)
        self.dialog.page.valueChanged.connect(self.searchPlus)
        self.dialog.limit.valueChanged.connect(self.searchPlus)

        self.dialog.next.clicked.connect(self.incPage)
        self.dialog.back.clicked.connect(self.decPage)
        self.dialog.back.setEnabled(False)
        self.dialog.exec_()
    
    @pyqtSlot(bool)
    def incPage(self,state):
        self.dialog.page.setValue(self.dialog.page.value()+1)

    @pyqtSlot(bool)
    def decPage(self,state):
        self.dialog.page.setValue(self.dialog.page.value()-1)

    @pyqtSlot(bool)
    def clearFields(self,state):
        self.searchModel.load_data(fields('user'))
        self.userModel.load_data(fields('user'))
        self.dialog.page.setValue(0)
        self.dialog.limit.setValue(15)
        self.resultModel.items.clear()
        self.resultModel.layoutChanged.emit()


    @pyqtSlot(int)
    def searchPlus(self,value):
        self.dialog.back.setEnabled(value > 0)
        self.search(True)

    @pyqtSlot(bool)
    def search(self,state):
        tmpData=dict()
        for key in self.searchModel.item.keys():
            if self.searchModel.item[key] != fields('user')[key]:
                tmpData[key]=self.searchModel.item[key]
        tmpData['page']=self.dialog.page.value()
        tmpData['limit']=self.dialog.limit.value()
        print(tmpData)
        #call search worker
        #update results view
        


    def prep_delegates(self,view):
        for num,k in enumerate(fields('user').keys()):
            if k in ['admin','active']:
                view.setItemDelegateForRow(num,CheckBoxDelegate(self))
            elif k in ['role','roles']:
                view.setItemDelegateForRow(num,ComboBoxDelegate(self,['user','admin']))
            
