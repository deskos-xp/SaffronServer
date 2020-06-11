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
from .workers.NewWorker import NewWorker
from .workers.Update import Update

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
        self.addressModel=ETM(item=fields("address"))

        setupViews(self,viewsList=['newUserEdit','departmentEdit','addressEdit'],modelsList=['userModel','departmentModel','addressModel'])
        for num,i in enumerate(self.userModel.item.keys()):
            if type(self.userModel.item[i]) == type(bool()):
                self.dialog.newUserEdit.setItemDelegateForRow(num,CheckBoxDelegate(self))

        self.dialog.newUserEdit.setItemDelegateForRow(len(fields('user').keys())-1,ComboBoxDelegate(self,data=['user','admin']))

        self.dialog.address_button_group.buttonClicked.connect(self.AddressButtonGroupAction)
        self.dialog.departments_button_group.buttonClicked.connect(self.DepartmentButtonGroupAction)

        self.addresses=[]
        self.departments=[]

        #QButtonGroup.
        self.states=[]

        self.dialog.addressExisting.currentIndexChanged.connect(self.store_selected)
        self.dialog.departmentExisting.currentIndexChanged.connect(self.store_selected)
        
        self.prepDepartmentLoader()
        self.prepAddressLoader()
        self.prepStateLoader()
                
        self.dialog.next.clicked.connect(self.advancePage)
        self.dialog.back.clicked.connect(self.fallBack)
        self.dialog.stackedWidget.currentChanged.connect(self.onChangedPage)
        self.dialog.back.setEnabled(False)
        self.dialog.save.setEnabled(False)
        self.dialog.save.clicked.connect(self.printModels)
        self.dialog.setWindowTitle("New U")
        self.dialog.exec_()

    def storeState(self,state):
        print(state)
        self.states.append(state)

    def statesLoaded(self):
        self.dialog.addressEdit.setItemDelegateForRow(1,ComboBoxDelegate(self,self.states))

    def printModels(self):
        for i in ['userModel','departmentModel','addressModel']:
            print(getattr(self,i).item)
        self.saveButtonClicked(True)

    def loadAddressOntoCombo(self,address):
        if address not in self.addresses:
            self.addresses.append(address)
        addressString=toAddressString(address)
        contained=[self.dialog.addressExisting.itemText(i) for i in range(self.dialog.addressExisting.count())]
        if addressString not in contained:
            self.dialog.addressExisting.addItem(addressString)

    def loadDepartmentOntoCombo(self,department):
        if department not in self.departments:
            self.departments.append(department)
        #departmentString=str(department)
        departmentString="{id}:{TYPE}: {displayable}".format(**dict(id=department.get("id"),TYPE="department",displayable=department.get("name")))
        contained=[self.dialog.departmentExisting.itemText(i) for i in range(self.dialog.departmentExisting.count())]
        if departmentString not in contained:
            self.dialog.departmentExisting.addItem(departmentString)
    uid=-1
    @pyqtSlot(bool)
    def saveButtonClicked(self,buttonState):
        def stage_3_modify(response):
            try:
                if response.status_code == 200:
                    j=response.json()
                    modAddress=Update(self.auth,dict(id=j.get("id")),"address",self.uid)
                    modAddress.signals.hasError.connect(lambda x:print(x))
                    modAddress.signals.hasResponse.connect(stage_complete)
                    modAddress.signals.finished.connect(lambda :print("finished adding address"))
                    QThreadPool.globalInstance().start(modAddress)

                    #modify user with new address id
                    #on hasResponse call stage_3
            except Exception as e:
                print(e)

        def stage_2(response):
            print(response)
            if response.status_code == 200:
                if self.dialog.newAddress.isChecked():
                    NewAddress=NewWorker(self.auth,self.addressModel.item,'address')
                    NewAddress.signals.hasError.connect(lambda x:print(x))
                    NewAddress.signals.hasResponse.connect(stage_3_modify)
                    NewAddress.signals.finished.connect(lambda: print("finished creating new address"))
                    QThreadPool.globalInstance().start(NewAddress)
                elif self.dialog.existingAddress.isChecked():
                    modAddress=Update(self.auth,self.addressModel.dataToItem(),"address",self.uid)
                    modAddress.signals.hasError.connect(lambda x:print(x))
                    modAddress.signals.hasResponse.connect(stage_complete)
                    modAddress.signals.finished.connect(lambda :print("finished adding address"))
                    QThreadPool.globalInstance().start(modAddress)
            else:
                raise Exception("response code for address not 200")

        def stage_complete(response):
            print(response)

        def stage_2_modify(response):
            try:
                if response.status_code == 200:
                    j=response.json()
                    if 'id' in j.keys():
                        modDepartment=Update(self.auth,dict(id=j.get('id')),"department",self.uid)
                        modDepartment.signals.hasError.connect(lambda x:print(x))
                        modDepartment.signals.hasResponse.connect(stage_2)
                        modDepartment.signals.finished.connect(lambda :print("finished adding department"))
                        QThreadPool.globalInstance().start(modDepartment) 
                    else:
                        raise Exception("missing id from response") 
                    #modify user with new department id
                    #on has response call stage_2
            except Exception as e:
                print(e)

        def stage_1(response):
            try:
                #print(response.json())
                if response.status_code == 200 and response.json().get("status") != 'old':
                    self.uid=response.json().get("id")
                    if self.dialog.newDepartment.isChecked():
                        NewDepartment=NewWorker(self.auth,self.departmentModel.item,"department")
                        NewDepartment.signals.hasError.connect(lambda x:print(x))
                        NewDepartment.signals.hasResponse.connect(stage_2_modify)
                        NewDepartment.signals.finished.connect(lambda:print("finished creating new department"))
                        QThreadPool.globalInstance().start(NewDepartment)
                    elif self.dialog.existingDepartment.isChecked():
                        modDepartment=Update(self.auth,self.departmentModel.dataToItem(),"department",self.uid)
                        modDepartment.signals.hasError.connect(lambda x:print(x))
                        modDepartment.signals.hasResponse.connect(stage_2)
                        modDepartment.signals.finished.connect(lambda :print("finished adding department"))
                        QThreadPool.globalInstance().start(modDepartment)
                    #modify department
                else:
                    raise Exception("response for department was not 200")
            except Exception as e:
                print(e)

        NewUserWorker=NewWorker(self.auth,self.userModel.item,"user")
        NewUserWorker.signals.hasError.connect(lambda x:print(x))
        NewUserWorker.signals.finished.connect(lambda: print("finished adding user details..."))
        NewUserWorker.signals.hasResponse.connect(stage_1)
        QThreadPool.globalInstance().start(NewUserWorker)

    def prepStateLoader(self):
        self.stateLoader=LoadStates()
        self.stateLoader.signals.hasError.connect(lambda x:print(x))
        self.stateLoader.signals.finished.connect(self.statesLoaded)
        self.stateLoader.signals.hasState.connect(self.storeState)
        QThreadPool.globalInstance().start(self.stateLoader)

    def prepDepartmentLoader(self):
        self.departmentLoader=getADRWorker(self.auth,"department")
        self.departmentLoader.signals.hasError.connect(lambda x:print(x))
        self.departmentLoader.signals.hasResponse.connect(lambda x:print(x))
        self.departmentLoader.signals.hasADR.connect(self.loadDepartmentOntoCombo)
        self.departmentLoader.signals.finished.connect(lambda : print("finished loading department"))
        QThreadPool.globalInstance().start(self.departmentLoader)

    def prepAddressLoader(self):
        self.addressLoader=getADRWorker(self.auth,"address")
        self.addressLoader.signals.hasError.connect(lambda x:print(x))
        self.addressLoader.signals.hasResponse.connect(lambda x:print(x))
        self.addressLoader.signals.hasADR.connect(self.loadAddressOntoCombo)
        self.addressLoader.signals.finished.connect(lambda : print("finished loading address"))
        QThreadPool.globalInstance().start(self.addressLoader)

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
            self.departmentModel.load_data(fields("department"))
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
            self.addressModel.load_data(fields("address"))
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
                    model.load_data(obj)
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
