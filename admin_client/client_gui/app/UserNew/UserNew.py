from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QHeaderView,QDialog,QWidget,QTableView
from PyQt5 import uic
from ..common.Fields import *
from ..common.editable_table_model import editable_table_model as ETM
from ..common.SetupModelView import setupViews
from .ModelDelegates import  CheckBoxDelegate,ComboBoxDelegate
from .workers.LoadStates import LoadStates
class UserNew(QDialog):
    def __init__(self,auth:dict,user:dict,parent:QWidget):
        super(UserNew,self).__init__()
        self.auth=auth
        self.user=user
        self.parent=parent

        self.dialog=QDialog()
        uic.loadUi("app/UserNew/forms/UserNew.ui",self.dialog)

        self.userModel=ETM(item=fields('user'))
        self.departmentModel=ETM(item=fields("department"))
        self.roleModel=ETM(item={})
        self.addressModel=ETM(item=fields("address"))

        setupViews(self,viewsList=['newUserEdit','departmentEdit','roleEdit','addressEdit'],modelsList=['userModel','departmentModel','roleModel','addressModel'])
        #self.dialog.newUserEditor.setModel(self.userModel)
        #self.dialog.newUserEditor.setItemDelegateFor
        for num,i in enumerate(self.userModel.item.keys()):
            if type(self.userModel.item[i]) == type(bool()):
                self.dialog.newUserEdit.setItemDelegateForRow(num,CheckBoxDelegate(self))

        self.states=[]
        def storeState(state):
            self.states.append(state)

        def statesLoaded():
            self.dialog.addressEdit.setItemDelegateForRow(1,ComboBoxDelegate(self,self.states))

        def printModels():
            for i in ['userModel','departmentModel','roleModel','addressModel']:
                print(getattr(self,i).item)
    
        
        self.stateLoader=LoadStates()
        self.stateLoader.signals.hasError.connect(lambda x:print(x))
        self.stateLoader.signals.finished.connect(statesLoaded)
        self.stateLoader.signals.hasState.connect(storeState)
        QThreadPool.globalInstance().start(self.stateLoader)

        
        self.dialog.next.clicked.connect(self.advancePage)
        self.dialog.back.clicked.connect(self.fallBack)
        self.dialog.stackedWidget.currentChanged.connect(self.onChangedPage)
        self.dialog.back.setEnabled(False)
        self.dialog.save.setEnabled(False)
        self.dialog.save.clicked.connect(printModels)
        self.dialog.setWindowTitle("New U")
        self.dialog.exec_()

    def onChangedPage(self,index):
        '''
        if index < self.dialog.stackedWidget.count():
            self.dialog.save.setEnabled(False)
        else:
            self.dialog.save.setEnabled(True)
        '''
        self.dialog.save.setEnabled(not (index < (self.dialog.stackedWidget.count()-1)))
        self.dialog.back.setEnabled(index > 0)
        self.dialog.next.setEnabled(index < (self.dialog.stackedWidget.count()-1))

    def advancePage(self):
        index=self.dialog.stackedWidget.currentIndex()
        if index < self.dialog.stackedWidget.count():
            index+=1
            self.dialog.stackedWidget.setCurrentIndex(index)
    
    def fallBack(self):
        index=self.dialog.stackedWidget.currentIndex()
        if index > 0:
            index-=1
            self.dialog.stackedWidget.setCurrentIndex(index)
