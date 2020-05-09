from PyQt5.QtCore import QCoreApplication,QThread,pyqtSignal
from PyQt5.QtWidgets import QDialog,QComboBox,QTextEdit
from .AddressComboBoxController import AddressComboBoxController
from .NewManufacturer import NewManufacturer
from .UpdateManufacturer import UpdateManufacturer
import string
class NewManufacturerDialogController(QDialog):
    manufacturer_address_add="{address}/manufacturer/update/{id}/add/address/{address_id}"
    auth:tuple=None
    #address:str=None
    w=None
    widget=None
    json:dict=dict(name="",comment="",phone="",email="")
    addressID:int=None
    comboData=[]
    jsonReady:pyqtSignal=pyqtSignal(dict,str)
    def __init__(self,widget,address,auth):
        self.widget=widget
        super(NewManufacturerDialogController,self).__init__()
        self.comboBox=AddressComboBoxController()
        self.comboBox.address=widget.address
        self.comboBox.finished.connect(self.finished_running)
        self.comboBox.newAddress.connect(self.add_new_address)
        self.comboBox.address=address
        self.comboBox.auth=auth
        widget.address.addItems(self.comboData)
        widget.address.currentTextChanged.connect(self.updateJson)
        widget.confirm.accepted.connect(self.confirmed)
        widget.confirm.rejected.connect(self.reject)
        widget.phone.textChanged.connect(self.limit_text_phone)
        widget.setWindowTitle("New Manufacturer")
        self.address=address
        widget.new_address.clicked.connect(self.create_new_address)
        self.comboBox.start()
        self.widget.finished.connect(self.comboBox.terminate)

    def limit_text_phone(self,text):
        print(len(text))
        if len(text) > 11:
            self.widget.confirm.setEnabled(False)
        else:
            self.widget.confirm.setEnabled(True)
            for char in text:
                if not char in string.digits+string.ascii_letters:
                    self.widget.confirm.setEnabled(False)
                    break

    def create_new_address(self):
        self.w.menu.add_new_address()
        self.addressID=self.w.menu.new_address_dialog_controller.addressId
        print(self.addressID)


    def reject(self):
        #print("rejeection")
        try:
            if self.comboBox.isRunning():
                self.comboBox.terminate()
        except Exception as e:
            print(e)
        self.widget.reject()

    def confirmed(self):
        self.comboBox.terminate()
        print(self.sender())
        tmp_json=dict()
        tmp_json['name']=self.widget.name.text()
        tmp_json['phone']=self.widget.phone.text()
        tmp_json['email']=self.widget.email.text()
        tmp_json['comment']=self.widget.comment.toPlainText()
        self.update=UpdateManufacturer()
        self.update.w=self.w
        self.update.widget=self.widget
        self.update.auth=self.w.auth
        self.update.address=self.w.address
       
        self.update.Updated.connect(lambda x: print(self.sender()))
            
        #json is now built, send to server to get manufacturer id
        self.manufacturer=NewManufacturer()
        self.manufacturer.w=self.w
        self.manufacturer.widget=self.widget
        self.manufacturer.auth=self.w.auth
        self.manufacturer.address=self.w.address
        self.manufacturer.json=tmp_json
        self.manufacturer.manufacturerSent.connect(self.setManufacturerID)
        self.manufacturer.start()
        #make a progress bar to indicate creation progress
        #disable all input on dialog until widget.address is fully populated

        
        #have address id
            
        #construct address string
        
        #send address update for manufacturer to server
        

        #print(tmp_address)
        #submit data
        self.widget.accept()
    
    def setManufacturerID(self,ID:int): 
            tmp_address=self.widget.address.currentText().split(":")[0]
            addr_str=self.manufacturer_address_add.format(**dict(address=self.address,id=ID,address_id=tmp_address))
            self.update.update_address=addr_str
            self.update.start()

    def finished_running(self):
        print(self.sender().objectName())

    def add_new_address(self,address:str):
        if address not in self.comboData:
            self.comboData.append(address)
            self.widget.address.clear()
            self.widget.address.addItems(self.comboData)
        #self.widget.address.update()
        #self.widget.address.addItem(address)

    def updateJson(self):
        obj=self.sender()
        n=obj.objectName()
        if n == "address":
            pass
        elif n == "name":
            self.json['name']=self.widget.name.text()
        elif n == "phone":
            self.json['phone']=self.widget.phone.text()
        elif n == "email":
            self.json['email']=self.widget.email.text()
        elif n == "comment":
            self.json["comment"]=self.widget.comment.text()
