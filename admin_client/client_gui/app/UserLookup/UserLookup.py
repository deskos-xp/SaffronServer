from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget,QHeaderView
import os,sys,json,ast,requests
from ..common.TableModel import TableModel
from ..common.editable_table_model import editable_table_model as ETM
from ..common.ModelDelegates import *
from ..common.Fields import * 
from ..common.Fields import fieldsUser as fields
from .ListModel import ListModel
from ..common.SetupModelView import setupViews
from .workers.ULookupSearch import ULookupSearch
import copy

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

        uic.loadUi("app/UserLookup/forms/viewForm.ui",self.dialog.result)
        self.dialog.result.frame.setEnabled(editableUser)
        self.dialog.result.department.clicked.connect(self.switchToDepartment)
        self.dialog.result.role.clicked.connect(self.switchToRole)
        self.dialog.result.address.clicked.connect(self.switchToAddress)
        #uic.loadUi("app/UserLookup/forms/viewForm.ui",self.dialog.department)
        #self.dialog.department.frame.setEnabled(editableUser)
        
        if editableUser == False:
            self.userModel=TableModel(item=fields("user"))
            self.dialog.result.frame.hide()
            #self.departmentModel=TableModel(item=fields("department"))
        else:
            self.userModel=ETM(item=fields("user"))
            #self.departmentModel=ETM(item=fields("department"))
            for num,i in enumerate(fields("user").keys()):
                if i in ['active','admin']:
                    self.dialog.result.userView.setItemDelegateForRow(num,CheckBoxDelegate(self))
            self.dialog.result.frame.show()
        

        #self.dialog.department.userView.setModel(self.departmentModel)
        #self.dialog.department.userView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.dialog.department.userView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.prep_delegates(self.dialog.searchView)        
        setupViews(self,viewsList=['searchView'],modelsList=['searchModel'])
        self.dialog.result.userView.setModel(self.userModel)
        self.dialog.result.userView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dialog.result.userView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.dialog.search_button.clicked.connect(self.search)
        self.dialog.clear.clicked.connect(self.clearFields)
        self.dialog.page.setValue(0)
        self.dialog.limit.setValue(15)
        self.dialog.page.valueChanged.connect(self.searchPlus)
        self.dialog.limit.valueChanged.connect(self.searchPlus)

        self.dialog.excluders.buttonClicked.connect(self.excludables_selected)

        self.dialog.result.save.clicked.connect(self.saveUser)
        self.dialog.result.home.clicked.connect(self.returnHome)

        self.dialog.next.clicked.connect(self.incPage)
        self.dialog.back.clicked.connect(self.decPage)
        self.dialog.back.setEnabled(False)

        self.prepViewsAndModels()

        self.dialog.exec_()

    def switchToAddress(self):
        p=getattr(self.dialog,'address')
        index=self.dialog.stackedWidget.indexOf(p)
        self.dialog.stackedWidget.setCurrentIndex(index)

    def switchToRole(self):
        p=getattr(self.dialog,'role')
        index=self.dialog.stackedWidget.indexOf(p)
        self.dialog.stackedWidget.setCurrentIndex(index)

    def switchToDepartment(self):
        p=getattr(self.dialog,"department")
        index=self.dialog.stackedWidget.indexOf(p)
        self.dialog.stackedWidget.setCurrentIndex(index)


    def prepViewsAndModels(self):
        self.models=dict()
        for i in ['departments','address','roles']:
            if self.editableUser == True:
                self.models[i]=ETM(item=dict())
            else:
                self.models[i]=TableModel(item=dict())
            w=None
            if i not in ['address']:
                w=getattr(self.dialog,i[:-1])
            else:
                w=getattr(self.dialog,i)
            
            uic.loadUi("app/UserLookup/forms/viewForm.ui",w)
            w.home.clicked.connect(self.returnToUserView)
            w.userView.setModel(self.models[i])
            w.userView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            w.userView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            w.role.clicked.connect(self.switchToRole)
            w.address.clicked.connect(self.switchToAddress)
            w.department.clicked.connect(self.switchToDepartment)
            w.frame.setEnabled(self.editableUser)
            if self.editableUser:
                w.frame.show()
            else:
                w.frame.hide()
            #print(self.models.keys(),'*?*'*30)

    def returnToUserView(self):
        w=getattr(self.dialog,"result")
        index=self.dialog.stackedWidget.indexOf(w)
        self.dialog.stackedWidget.setCurrentIndex(index)

    @pyqtSlot(bool)
    def saveUser(self,state):
        print(self.userModel.item)

    @pyqtSlot(bool)
    def returnHome(self,state):
        self.dialog.stackedWidget.setCurrentIndex(0)

    def resultsPeeping(self,index):
        print(self.resultModel.items[index.row()])
        '''
        for num,i in enumerate(self.userModel.item.keys()):
            if i in ['departments']:
                #print("making department delegate")
                #print(num)
                def doIt(x):
                    print(self.userModel.item.get("departments"))
                    self.departmentModel.load_data(self.userModel.item.get('departments')[0])
                    self.dialog.stackedWidget.setCurrentIndex(2)

                self.dialog.result.userView.setItemDelegateForRow(num-1,ButtonDelegate(self,doIt,i))
        '''
                
        self.models['roles'].load_data(self.resultModel.items[index.row()].get("roles"))
        self.models['departments'].load_data(self.resultModel.items[index.row()].get("departments"))
        #print(self.dialog.department.userView.model().item," departments"*10)
        self.models['address'].load_data(self.resultModel.items[index.row()].get("address"))
        
        tmp=copy.deepcopy(self.resultModel.items[index.row()])
        tmp.__delitem__("roles")
        tmp.__delitem__("address")
        tmp.__delitem__("departments")
        
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
        print(user.keys())
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
            
