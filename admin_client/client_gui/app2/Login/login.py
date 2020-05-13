from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QObject,pyqtSignal,QRunnable,pyqtSlot,QCoreApplication
from PyQt5.QtWidgets import QTextEdit,QPushButton,QStackedWidget,QMainWindow,QApplication,QWidget
import sys
from .worker import Worker
class Login(QWidget):
    #address="http://localhost:9000/"
    #auth=("admin","avalon")
    login:dict=dict(username=None,password=None,server_address=None)
    widget:QWidget=None
    loggedIn:pyqtSignal=pyqtSignal(dict)
    def __init__(self,widget):
        super(Login,self).__init__()
        self.widget=widget
        uic.loadUi("app2/Login/forms/login.ui",self.widget)
        
        self.widget.username.textChanged.connect(self.saveLogin)
        self.widget.password.textChanged.connect(self.saveLogin)
        self.widget.server_address.textChanged.connect(self.saveLogin)

        self.widget.login.clicked.connect(self.attemptLogin)
        self.qtp=QThreadPool.globalInstance() 

    def attemptLogin(self):
        self.worker=Worker(self.login)
        self.worker.signals.state.connect(self.loginState)
        self.qtp.start(self.worker)

    def loginState(self,boolean):
        print(boolean)
        if boolean == True:
            self.loggedIn.emit(self.login)

    @pyqtSlot(str)
    def saveLogin(self,text):
        self.login[self.sender().objectName()]=text
