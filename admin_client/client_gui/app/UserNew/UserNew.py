from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QHeaderView,QDialog,QWidget,QTableView,QButtonGroup,QComboBox
from PyQt5 import uic
from ..common.Fields import *
from ..common.editable_table_model import editable_table_model as ETM
from ..common.SetupModelView import setupViews
from .ModelDelegates import  CheckBoxDelegate,ComboBoxDelegate
from .workers.LoadStates import LoadStates
from .workers.NewU import NewU
from .workers.getADRWorker import getADRWorker

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
        self.roleModel=ETM(item=dict(roles="user"))
        self.addressModel=ETM(item=fields("address"))

        setupViews(self,viewsList=['newUserEdit','departmentEdit','roleEdit','addressEdit'],modelsList=['userModel','departmentModel','roleModel','addressModel'])
        #self.dialog.newUserEditor.setModel(self.userModel)
        #self.dialog.newUserEditor.setItemDelegateFor
        for num,i in enumerate(self.userModel.item.keys()):
            if type(self.userModel.item[i]) == type(bool()):
                self.dialog.newUserEdit.setItemDelegateForRow(num,CheckBoxDelegate(self))

        self.dialog.roleEdit.setItemDelegateForRow(0,ComboBoxDelegate(self,data=["user","admin"]))
       
        self.dialog.address_button_group.buttonClicked.connect(self.AddressButtonGroupAction)
        self.dialog.departments_button_group.buttonClicked.connect(self.DepartmentButtonGroupAction)

        self.addresses=[]
        self.departments=[]

        #QButtonGroup.
        self.states=[]
        def storeState(state):
            self.states.append(state)

        def statesLoaded():
            self.dialog.addressEdit.setItemDelegateForRow(1,ComboBoxDelegate(self,self.states))

        def printModels():
            for i in ['userModel','departmentModel','roleModel','addressModel']:
                print(getattr(self,i).item)

        def loadAddressOntoCombo(address):
            if address not in self.addresses:
                self.addresses.append(address)
            addressString=toAddressString(address)
            contained=[self.dialog.addressExisting.itemText(i) for i in range(self.dialog.addressExisting.count())]
            if addressString not in contained:
                self.dialog.addressExisting.addItem(addressString)

        def loadDepartmentOntoCombo(department):
            if department not in self.departments:
                self.departments.append(department)
            #departmentString=str(department)
            departmentString="{id}:{TYPE}: {displayable}".format(**dict(id=department.get("id"),TYPE="department",displayable=department.get("name")))
            contained=[self.dialog.departmentExisting.itemText(i) for i in range(self.dialog.departmentExisting.count())]
            if departmentString not in contained:
                self.dialog.departmentExisting.addItem(departmentString)



        self.dialog.addressExisting.currentIndexChanged.connect(self.store_selected)
        self.dialog.departmentExisting.currentIndexChanged.connect(self.store_selected)

        self.departmentLoader=getADRWorker(self.auth,"department")
        self.departmentLoader.signals.hasError.connect(lambda x:print(x))
        self.departmentLoader.signals.hasResponse.connect(lambda x:print(x))
        self.departmentLoader.signals.hasADR.connect(loadDepartmentOntoCombo)
        self.departmentLoader.signals.finished.connect(lambda : print("finished loading department"))
        QThreadPool.globalInstance().start(self.departmentLoader)

        self.addressLoader=getADRWorker(self.auth,"address")
        self.addressLoader.signals.hasError.connect(lambda x:print(x))
        self.addressLoader.signals.hasResponse.connect(lambda x:print(x))
        self.addressLoader.signals.hasADR.connect(loadAddressOntoCombo)
        self.addressLoader.signals.finished.connect(lambda : print("finished loading address"))
        QThreadPool.globalInstance().start(self.addressLoader)

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

    def store_selected(self,index):
        item=regexThisShit2(self.sender().itemText(index))
        name=self.sender().objectName()
        name=name.replace("Existing","")
        name=name.replace("New","")
        name=name.lower()
        print(name)
        if name == "address":   
            for address in getattr(self,"addresses"):
                if int(item.get("ID")) == address.get("id"):
                    getattr(self,name+"Model").item=address
                    getattr(self,name+"Model").layoutChanged.emit()
                    break
        else:
            for obj in getattr(self,name+"s"):
                try:
                    if int(item.get("ID")) == obj.get("id"):
                        getattr(self,name+"Model").item=obj
                        getattr(self,name+"Model").layoutChanged.emit()
                        break
                except Exception as e:
                    print(e)
                    print(item)

    def DepartmentButtonGroupAction(self,button):
        obj_name=self.sender().checkedButton().objectName()
        print(obj_name)
        if obj_name == "newDepartment":
            getattr(self.dialog,"departmentEdit").setEnabled(True)
            getattr(self.dialog,"departmentExisting").setEnabled(False)
            self.departmentModel.item=fields("address")
        elif obj_name == "existingDepartment":
            getattr(self.dialog,"departmentExisting").setEnabled(True)
            getattr(self.dialog,"departmentEdit").setEnabled(False)
            self.ComboToModel(self.dialog.departmentExisting,self.departments,self.departmentModel)
 
    def AddressButtonGroupAction(self,button):
        obj_name=self.sender().checkedButton().objectName()
        print(obj_name)
        if obj_name == "newAddress":
            getattr(self.dialog,"addressEdit").setEnabled(True)
            getattr(self.dialog,"addressExisting").setEnabled(False)
            self.addressModel.item=fields("address")
        elif obj_name == "existingAddress":
            getattr(self.dialog,"addressExisting").setEnabled(True)
            getattr(self.dialog,"addressEdit").setEnabled(False)
            self.ComboToModel(self.dialog.addressExisting,self.addresses,self.addressModel)
     
    def ComboToModel(self,combo,contained,model):
        item=regexThisShit2(combo.currentText())
        if item != None:
            ID=int(item.get("ID"))
            for obj in contained:
                if obj.get("id") == ID:
                    model.item=obj
                    model.layoutChanged.emit()
                    break

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
