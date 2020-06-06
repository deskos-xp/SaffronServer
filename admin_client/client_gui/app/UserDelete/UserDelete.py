from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog,QWidget,QComboBox,QDialogButtonBox
from .TableModel import TableModel
from ..common.Fields import *
from ..common.SetupModelView import setupViews
import os,sys,json,requests
from .workers.GetUsers import GetUsers
from .workers.DeleteUserWorker import DeleteUserWorker
from ..common.ModelDelegates import ComboBoxDelegate,LineEditDelegate 
class UserDelete(QDialog):
    def __init__(self,auth:dict,parent:QWidget):
        self.auth=auth
        self.parent=parent
        super(UserDelete,self).__init__()
        self.dialog=QDialog()
        uic.loadUi("app/UserDelete/forms/UserDelete.ui",self.dialog)
        self.users=[]
        self.userModel=TableModel(item=fields("user"))
        self.dialog.userView.setModel(self.userModel)

        self.dialog.deleteUser.clicked.connect(self.deleteUserInModel)

        setupViews(self,viewsList=['userView'],modelsList=['userModel'])

        self.dialog.users.currentIndexChanged.connect(self.updateModel)
        self.prepGetUsersWorker()



        self.dialog.exec_()

    @pyqtSlot(bool)
    def deleteUserInModel(self,state):
        print(self.userModel.item)
        if self.userModel.item.get("id") != None:
            deleteUser=DeleteUserWorker(self.auth,self.userModel.item)
            deleteUser.signals.hasError.connect(lambda x:print(x))
            deleteUser.signals.finished.connect(self.resetUsersCombo)
            deleteUser.signals.hasResponse.connect(lambda x:print(x))
            QThreadPool.globalInstance().start(deleteUser)
        
    def updateModel(self,index):
        WHO=self.dialog.users.itemText(index)
        WHO=regexThisShit2(WHO)
        if WHO == None:
            return
        for u in self.users:
            if u.get("id") == int(WHO.get("ID")):
                self.userModel.load_data(u)
                self.userModel.layoutChanged.emit()
                break

    def resetUsersCombo(self):
        print("finished deleting user... now updating relavent widgets...")
        self.users.clear()
        self.dialog.users.clear()
        self.prepGetUsersWorker()

    @pyqtSlot(dict)
    def updateUsersCombo(self,user):
        if user not in self.users:
            self.users.append(user)
        contained=[self.dialog.users.itemText(i) for i in range(self.dialog.users.count())]
        uString="{id}:user - {uname} [{fname} {mname} {lname}]".format(**user)
        if uString not in contained:        
            contained.append(uString)
        self.dialog.users.clear()
        self.dialog.users.addItems(contained)
    
    def prepGetUsersWorker(self):
        self.getUsersWorker=GetUsers(self.auth)
        self.getUsersWorker.signals.hasError.connect(lambda x:print(x))
        self.getUsersWorker.signals.hasResponse.connect(lambda x:print(x))
        self.getUsersWorker.signals.hasUser.connect(self.updateUsersCombo)
        QThreadPool.globalInstance().start(self.getUsersWorker)
