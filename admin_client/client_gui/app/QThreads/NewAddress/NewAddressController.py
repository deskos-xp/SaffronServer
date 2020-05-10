from PyQt5.QtCore import QThread,QCoreApplication
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog,QWidget,QPushButton,QComboBox
import os,sys,time,requests,json
from .StateComboBoxController import StateComboBoxController
from .Sender import Sender
class NewAddressController(QDialog):
    auth:tuple=None
    address:str=None
    w=None
    widget=None
    json=dict(state="",city="",ZIP="",street_name="",street_number=0)
    addressId:int=None
    def __init__(self,widget):
        super(NewAddressController,self).__init__()
        self.widget=widget
        self.widget.setWindowTitle("New Address")
        self.comboBox=StateComboBoxController()
        self.comboBox.widget=widget.state
        self.comboBox.finished.connect(self.finished_reading_conf)
        self.comboBox.newState.connect(self.add_new_from_conf)
        self.widget.state.currentTextChanged.connect(self.updateJson)
        self.comboBox.start()

        self.widget.street_number.valueChanged.connect(self.updateJson)
        self.widget.street_name.textChanged.connect(self.updateJson)
        self.widget.city.textChanged.connect(self.updateJson)
        self.widget.ZIP.textChanged.connect(self.updateJson)
        self.widget.apartment.textChanged.connect(self.updateJson)

        self.widget.confirm.accepted.connect(self.sendData)


    def sendData(self):
        #print(self.json)
        self.senderData=Sender(auth=self.auth,address=self.address)
        self.senderData.finished.connect(self.finished)
        self.senderData.json=self.json
        self.senderData.w=self.w
        self.senderData.statusSig.connect(self.finished_msg_display)
        self.senderData.start() 
        self.widget.accept()

    def finished_msg_display(self,status):
        self.w.statusBar().showMessage(str(status.status_code)+" : AddressID is {addressID}".format(**dict(addressID=status.json().get("id"))))
        self.addressID=status.json().get("id")
        print(status,": AddressID is {addressID}".format(**dict(addressID=self.addressID)))


    def finished(self):
        print(self.sender().objectName())
    
    def finished_reading_conf(self):
        pass

    def add_new_from_conf(self,text):
        self.widget.state.addItem(text)

    def updateJson(self):
        obj=self.sender()
        n=obj.objectName()
        if n == "state":
            self.json['state']=obj.currentText().split(" - ")[1]
        elif n == "city":
            self.json['city']=obj.text()
        elif n == "ZIP":
            self.json['ZIP']=obj.text()
        elif n == "street_number":
            self.json['street_number']=obj.value()
        elif n == "street_name":
            self.json['street_name']=obj.text()
