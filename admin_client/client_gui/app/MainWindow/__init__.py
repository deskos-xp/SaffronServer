from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QObject,pyqtSignal,QRunnable,pyqtSlot,QCoreApplication,pyqtSlot
from PyQt5.QtWidgets import QTextEdit,QPushButton,QStackedWidget,QMainWindow,QApplication
import sys

from ..Login import login 
from ..NewProduct.NewProduct import NewProduct
from ..SearchProduct.SearchProduct import SearchProduct
from ..drm import drm,drmEnum
from PyQt5.QtCore import QCoreApplication

class Main(QMainWindow,QObject):
    #address="http://localhost:9000/"
    #auth=("admin","avalon")
    auth:dict=dict(server_address=None,username=None,password=None)
    EXIT_CODE_REBOOT = 33333333
    def __init__(self):
        super(Main,self).__init__()
        uic.loadUi("app/MainWindow/forms/app.ui",self)
        self.Login=login.Login(self.login)

        self.setWindowTitle("SaffronClient 2")
        #self.setWindowIcon(Icon(PATH))
        self.qtp=QThreadPool.globalInstance()
        self.sb=self.statusBar()
        self.Login.loggedIn.connect(self.stackChange)
        
        self.application.currentChanged.connect(self.readyToWork)
        d=drm()
        if d.state == drmEnum.LOCKED:
            exit() 
            print(d.state)
        #self.show()


    def readyToWork(self):
        self.newGrid=NewProduct(self.auth,self.newGrid)
        self.searchGrid=SearchProduct(self.auth,self.searchGrid)

    @pyqtSlot(dict)
    def stackChange(self,auth:dict):
        self.auth=auth
        self.application.setCurrentIndex(1)


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


