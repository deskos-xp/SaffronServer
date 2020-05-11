import sys
from PyQt5 import QtGui,uic
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,qApp,QStackedWidget
from app import SearchGrid,NewGrid,CredentialController
import faulthandler
faulthandler.enable()
from PyQt5.QtCore import pyqtSignal,QObject,pyqtSlot,QCoreApplication
from app.MenuBar import MenuBar
class mainWindow(QMainWindow,QObject):
    #address="http://localhost:9000/"
    #auth=("admin","avalon")
    auth:tuple=None
    address:str=None
    EXIT_CODE_REBOOT = 33333333
    STACKED_INDEX=None
    stackedWidgetChange=pyqtSignal(int)
    def reboot(self):
        QCoreApplication.exit(self.EXIT_CODE_REBOOT)
        self.destroy()
    def __init__(self):
        super(mainWindow,self).__init__() 
        #QStackedWidget.
        uic.loadUi('app/forms/MainWindow.ui',self)
        uic.loadUi('app/forms/SearchGrid.ui',self.search_widget)
        uic.loadUi('app/forms/NewGrid.ui',self.new_widget)
        uic.loadUi('app/forms/Credentials.ui',self.credential_holder)
        self.setWindowTitle("Saffron Explorer")
        self.setWindowIcon(QIcon("app/Icons/SaffronExplorer.png"))
        self.search_widget.root=self
        self.new_widget.root=self
        self.credential_holder.root=self
        self.sb=self.statusBar()

        self.STACKED_INDEX={self.stackedWidget.widget(i).objectName():i for i in range(self.stackedWidget.count())}
        self.stackedWidgetChange.connect(self.changeWidget)
        self.label_loading.setPixmap(QPixmap("app/Icons/SaffronExplorer.png"))


        self.cred_controller=CredentialController.CredentialController(self.credential_holder)
        self.cred_controller.haveCredentials.connect(self.ready_creds)
        self.cred_controller.getConfig_values()
        self.ng_controller=NewGrid.NewGrid(self.new_widget,self.auth,self.address) 
        #self.ng_controller.address=self.address
        #self.ng_controller.auth=self.auth

        self.sg_controller=SearchGrid.SearchViewGrid(self.search_widget,self.auth,self.address)
        #self.sg_controller.address=self.address
        #self.sg_controller.auth=self.auth


        self.menu=MenuBar(w=self)
        self.show() 
        #self.menuBar()


    def changeWidget(self,index): 
        self.stackedWidget.setCurrentIndex(index)

    def ready_creds(self,auth,address):
        self.address=address
        self.auth=auth
        self.reboot()
        '''
        try:
            self.ng_controller.__init__(self.new_widget,self.auth,self.address) 
            self.sg_controller.__init__(self.search_widget,self.auth,self.address)
        except Exception as e:
            print(e)
        '''

def main():
    #ecode=mainWindow.EXIT_CODE_REBOOT
    #while ecode == mainWindow.EXIT_CODE_REBOOT:
    ecode=0
    app = QApplication(sys.argv)
    ex=mainWindow() 
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
