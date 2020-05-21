from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QObject,pyqtSignal,QRunnable,pyqtSlot,QCoreApplication,pyqtSlot
from PyQt5.QtWidgets import QTextEdit,QPushButton,QStackedWidget,QMainWindow,QApplication
import sys
from .MenuBar.MenuBar import MenuBar
from PyQt5.QtGui import QIcon,QPixmap,QImage

from ..Login.login import Login 
from ..NewProduct.NewProduct import NewProduct
from ..SearchProduct.SearchProduct import SearchProduct
from ..drm import drm,drmEnum
from PyQt5.QtCore import QCoreApplication
import json
from ..Icons import *

class Main(QMainWindow,QObject):
    auth:dict=dict(server_address=None,username=None,password=None)
    EXIT_CODE_REBOOT = 33333333
    def loadFromAbout(self,file):
        buff=dict()
        with open(file,"r") as fd:
            buff=json.load(fd)
        return buff


    def __init__(self):
        super(Main,self).__init__()
        uic.loadUi("app/MainWindow/forms/app.ui",self)
        self.loggin=Login(self.login)
        self.setWindowTitle(self.loadFromAbout("app/About/about.json").get("Name"))
        pix=getProgram_image(self.loadFromAbout("app/About/about.json").get("icon"))
        
        icon=QIcon(QPixmap.fromImage(QImage.fromData(pix.read())))
        self.setWindowIcon(icon)
        self.sb=self.statusBar()
        self.loggin.loggedIn.connect(self.stackChange)
        self.loggin.logInFail.connect(self.logInFailed)
        self.application.currentChanged.connect(self.readyToWork)
        
        self.menubar=MenuBar(self,self.auth)        
       
        d=drm()
        if d.state == drmEnum.LOCKED:
            exit(d.state) 
            print(d.state)
        #self.show()

    @pyqtSlot()
    def logInFailed(self):
        self.sb.showMessage("Attempted Log-In failed!",1000)

    @pyqtSlot()
    def readyToWork(self):
        self.menubar.loggedIn(self.application.currentIndex())
        self.newGrid=NewProduct(self.auth,self.newGrid)
        self.searchGrid=SearchProduct(self.auth,self.searchGrid)

    @pyqtSlot(dict)
    def stackChange(self,auth:dict):
        self.auth=auth
        self.application.setCurrentIndex(1)
        self.menubar.auth=auth

'''
def main():
    #ecode=mainWindow.EXIT_CODE_REBOOT
    #while ecode == mainWindow.EXIT_CODE_REBOOT:
    ecode=0
    app = QApplication(sys.argv)
    ex=Main()
    ex.show()
    ecode=app.exec_()
    return ecode




if __name__ == "__main__":
    ecode=0
    while True:
        ecode=main()       
        if ecode != mainWindow.EXIT_CODE_REBOOT:
            break
        print(ecode)
        del(ecode)
        ecode=0
'''

