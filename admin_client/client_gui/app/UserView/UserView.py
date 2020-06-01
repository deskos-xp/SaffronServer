from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog,QHeaderView
import os,sys,json,requests
import copy
from ..common.Fields import *
from ..common.TableModel import TableModel

class UserView(QDialog):
    def __init__(self,auth:dict,user:dict,parent):
        super(UserView,self).__init__()
        self.auth=auth
        
        self.parent=parent
        self.dialog=QDialog()
        uic.loadUi("app/UserView/forms/UserView.ui",self.dialog)
        self.dialog.setWindowTitle("User View...")
        
        self.role=firstBorn(copy.deepcopy(user.get("roles")))
        self.department=firstBorn(copy.deepcopy(user.get("departments")))
        self.address=firstBorn(copy.deepcopy(user.get("address")))
        tmp=copy.deepcopy(user)
        tmp.__delitem__("roles")
        tmp.__delitem__("departments")
        tmp.__delitem__("address")
        self.user=tmp
        del(tmp)
    
        self.userModel=TableModel(item=self.user)
        self.addressModel=TableModel(item=self.address)
        self.departmentModel=TableModel(item=self.department)
        self.roleModel=TableModel(item=self.role)

        def setupViews(view,model):
            view.setModel(model)
            view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        views=['userView','addressView','departmentView','roleView']
        models=['userModel','addressModel','departmentModel','roleModel']

        for v,m in zip(views,models):
            view=getattr(self.dialog,v)
            model=getattr(self,m)
            setupViews(view,model)

        self.dialog.back.clicked.connect(self.return_home)
        self.dialog.Address.clicked.connect(self.goToPage)
        self.dialog.Department.clicked.connect(self.goToPage)
        self.dialog.Role.clicked.connect(self.goToPage)

        self.dialog.exec_()

    def goToPage(self):
        name=self.sender().objectName()
        name="{name}Info".format(**dict(name=name))
        page=getattr(self.dialog,name)
        index=self.dialog.stackedWidget.indexOf(page)
        if self.dialog.stackedWidget.currentIndex() != index:
            self.dialog.stackedWidget.setCurrentIndex(index)
    
    def return_home(self):
        if self.dialog.stackedWidget.currentIndex() != 0:
            userStack=getattr(self.dialog,'UserInfo')
            index=self.dialog.stackedWidget.indexOf(userStack)
            self.dialog.stackedWidget.setCurrentIndex(index)
   
