from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json,ast,requests
from ..common.TableModel import TableModel
from ..common.editable_table_model import editable_table_model as ETM
from ..common.ModelDelegates import *
from ..common.Fields import * 
from ..common.Fields import fieldsUser as fields
from .ListModel import ListModel
from ..common.SetupModelView import setupViews
from .workers.ULookupSearch import ULookupSearch

class UserLookup(QDialog):
    def __init__(self,auth:dict,parent:QWidget,editableUser=False):
        super(UserLookup,self).__init__()
        self.auth=auth
        self.parent=parent
        self.dialog=QDialog()
        self.editableUser=editableUser
        uic.loadUi("app/UserLookup/forms/UserLookup.ui",self.dialog)
       
        self.excludables=[]
 
        self.searchModel=ETM(item=fields("user")) 
        self.resultModel=ListModel(TYPE='user',items=[])
        self.dialog.resultsView.setModel(self.resultModel)
        self.dialog.resultsView.activated.connect(self.resultsPeeping)

        self.dialog.frame.setEnabled(editableUser)
        
        if editableUser == False:
            self.userModel=TableModel(item=fields("user"))
            self.dialog.frame.hide()
        else:
            self.userModel=ETM(item=fields("user"))
            self.dialog.frame.show()
                
        self.prep_delegates(self.dialog.searchView)        
        setupViews(self,viewsList=['searchView','userView'],modelsList=['searchModel','userModel'])

        self.dialog.search_button.clicked.connect(self.search)
        self.dialog.clear.clicked.connect(self.clearFields)
        self.dialog.page.setValue(0)
        self.dialog.limit.setValue(15)
        self.dialog.page.valueChanged.connect(self.searchPlus)
        self.dialog.limit.valueChanged.connect(self.searchPlus)

        self.dialog.excluders.buttonClicked.connect(self.excludables_selected)

        self.dialog.home.clicked.connect(self.returnHome)
        self.dialog.next.clicked.connect(self.incPage)
        self.dialog.back.clicked.connect(self.decPage)
        self.dialog.back.setEnabled(False)
        self.dialog.exec_()

    @pyqtSlot(bool)
    def returnHome(self,state):
        self.dialog.stackedWidget.setCurrentIndex(0)

    def resultsPeeping(self,index):
        self.userModel.load_data(self.resultModel.items[index.row()])
        self.dialog.stackedWidget.setCurrentIndex(1)

    def excludables_selected(self,button):
        n=button.objectName().replace("exclude_","").lower()
        if button.isChecked():
            if n not in self.excludables:
                self.excludables.append(n)
        else:
            if n in self.excludables:
                self.excludables.remove(n)

    def searchWorker(self,terms):
        self.resultModel.items.clear()
        self.resultModel.layoutChanged.emit()
        searchWorker=ULookupSearch(self.auth,terms)
        searchWorker.signals.hasError.connect(lambda x:print(x))
        searchWorker.signals.hasUser.connect(self.hasUserAction)
        searchWorker.signals.finished.connect(lambda : print("finished search for users!"))
        QThreadPool.globalInstance().start(searchWorker)

    @pyqtSlot(dict)
    def hasUserAction(self,user):
        self.resultModel.items.append(user)
        self.resultModel.layoutChanged.emit()
        #print(user) 
   
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
        self.excludables.clear()
        self.dialog.exclude_admin.setChecked(False)
        self.dialog.exclude_active.setChecked(False)

    @pyqtSlot(int)
    def searchPlus(self,value):
        self.dialog.back.setEnabled(value > 0)
        self.search(True)

    @pyqtSlot(bool)
    def search(self,state):
        tmpData=dict()
        for key in self.searchModel.item.keys():
            #print(key in self.excludables)
            if key not in self.excludables:
                if self.searchModel.item[key] != fields('user')[key]:
                    tmpData[key]=self.searchModel.item[key]
            else:
                tmpData[key]=self.searchModel.item[key]
        tmpData['page']=self.dialog.page.value()
        tmpData['limit']=self.dialog.limit.value()
        #print(tmpData.keys())
        #print(self.excludables)
        self.searchWorker(tmpData)
        #call search worker
        #update results view
        

    def prep_delegates(self,view):
        for num,k in enumerate(fields('user').keys()):
            if k in ['admin','active']:
                view.setItemDelegateForRow(num,CheckBoxDelegate(self))
            elif k in ['role','roles']:
                view.setItemDelegateForRow(num,ComboBoxDelegate(self,['user','admin']))
            
