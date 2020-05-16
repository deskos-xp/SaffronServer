from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QObject,pyqtSignal,QRunnable,pyqtSlot,QCoreApplication
from PyQt5.QtWidgets import QTextEdit,QPushButton,QStackedWidget,QMainWindow,QApplication,QWidget,QCheckBox
import sys
from .workers.worker import Worker
from .workers.saveAuth import SaveAuth
from .workers.loadAuth import LoadAuth
class Login(QWidget):
    #address="http://localhost:9000/"
    #auth=("admin","avalon")
    auth:dict=dict(username=None,password=None,server_address=None)
    widget:QWidget=None
    loggedIn:pyqtSignal=pyqtSignal(dict)
    credfile="creds.json"
    def __init__(self,widget):
        super(Login,self).__init__()
        self.widget=widget
        uic.loadUi("app/Login/forms/login.ui",self.widget)
        
        self.widget.username.textChanged.connect(self.saveLogin)
        self.widget.password.textChanged.connect(self.saveLogin)
        self.widget.server_address.textChanged.connect(self.saveLogin)
        self.widget.rememberMe.toggled.connect(self.handleSave)
        self.widget.login.clicked.connect(self.attemptLogin)
        
        self.qtp=QThreadPool.globalInstance() 
        
        l=LoadAuth(self.widget,self.credfile)
        self.qtp.start(l)

    def notify(self,error):
        print(error)

    def handleSave(self,state):
        if state == False:
            a=dict(self.auth)
            for i in a.keys():
                a[i]=None
            sauth=SaveAuth(a,self.credfile)
            self.qtp.start(sauth)

    def attemptLogin(self):
        if self.widget.rememberMe.isChecked() == True:
            sauth=SaveAuth(self.auth,self.credfile)
            self.qtp.start(sauth)
        self.worker=Worker(self.auth)
        self.worker.signals.state.connect(self.loginState)
        self.worker.signals.hasError.connect(self.notify)
        self.qtp.start(self.worker)

    def loginState(self,boolean):
        print(boolean)
        if boolean == True:
            self.loggedIn.emit(self.auth)

    @pyqtSlot(str)
    def saveLogin(self,text):
        self.auth[self.sender().objectName()]=text
