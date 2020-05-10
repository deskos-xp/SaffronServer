from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
from PyQt5.QtWidgets import QWidget,QLineEdit,QPushButton,qApp
import os,json
from app.QThreads.TestConnection import Check
from dotenv import load_dotenv
load_dotenv()

class CredentialController(QWidget,QThread):
    auth:list=["",""]
    address:str=None
    widget=None
    default_config:str=os.getenv("default_config")
    conf_data:dict=None
    saveDone:pyqtSignal=pyqtSignal()
    loadDone:pyqtSignal=pyqtSignal()
    haveCredentials:pyqtSignal=pyqtSignal(tuple,str)

    def __init__(self,widget):
        super(CredentialController,self).__init__()
        self.widget=widget

        widget.address.textChanged.connect(self.text_changed)
        widget.username.textChanged.connect(self.text_changed)
        widget.password.textChanged.connect(self.text_changed)
        widget.save_credentials.clicked.connect(self.saveConfig_values)
        self.saveDone.connect(self.set_globals)
        
        self.testConnection=Check()
        self.testConnection.widget=self.widget
        self.testConnection.status.connect(self.display_status) 
        widget.test_connection.clicked.connect(self.testConnection.start)
        
        self.getConfig_values()
        self.loadDone.connect(self.set_globals)

    def display_status(self,status_code):
        print(status_code)

    def set_globals(self):
        self.auth[0]=self.widget.username.text()
        self.auth[1]=self.widget.password.text()
        self.address=self.widget.address.text()
        self.haveCredentials.emit(tuple(self.auth),self.address)
        #qApp.exit(self.widget.root.EXIT_CODE_REBOOT)
        self.widget.root.reboot()
    def saveConfig_values(self): 
        self.conf_data['address']=self.widget.address.text()
        self.conf_data['username']=self.widget.username.text()
        self.conf_data['password']=self.widget.password.text()
        with open(self.default_config,"w") as ofile:
            json.dump(self.conf_data,ofile)
        self.saveDone.emit()

    def getConfig_values(self):
        with open(self.default_config,"r") as ifile:
            self.conf_data=json.load(ifile)
        print(self.conf_data)
        self.widget.address.setText(self.conf_data.get("address"))
        self.widget.password.setText(self.conf_data.get("password"))
        self.widget.username.setText(self.conf_data.get("username"))
        self.loadDone.emit()

    def text_changed(self,text):
        edit=self.sender()
        if edit.objectName() == "address":
            self.address=edit.text()
        elif edit.objectName() in ['username','password']:
            if edit.objectName() == "username":
                self.auth[0]=edit.text()
            elif edit.objectName() == "password":
                self.auth[1]=edit.text()
            else:
                raise BaseException(edit.objectName())
        else:
            raise BaseException(edit.text())


