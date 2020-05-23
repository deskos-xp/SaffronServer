from PyQt5.QtCore import QObject,QThread,QThreadPool,pyqtSignal,pyqtSlot,QCoreApplication,QModelIndex
from PyQt5.QtWidgets import QWidget,QStackedWidget
#from . import About
app=__import__(__name__.split('.')[0])
from app.About.about import About
from app.DeleteDialog_rev2 import DeleteDialog
from app.NewEntity.NewEntity import NewEntity

#print("top package --->",app)
class MenuBar:
    def __init__(self,mainWindow:QWidget,auth):
        self.auth=auth
        self.mainWindow=mainWindow
        self.mainWindow.actionLogout.triggered.connect(self.logOut) 
        if self.mainWindow.application.currentIndex() < 1:
            self.mainWindow.actionLogout.setEnabled(False)
        self.mainWindow.action_About.triggered.connect(self.about_)        
        self.mainWindow.actionDelete.triggered.connect(self.delete_)
        self.mainWindow.action_New.triggered.connect(self.new_)
        #QStackedWidget
        self.mainWindow.application.currentChanged.connect(self.notLoggedIn)

    def notLoggedIn(self,index):
        print(index)
        state=not index==0
        self.mainWindow.actionEdit.setEnabled(state)
        self.mainWindow.actionDelete.setEnabled(state)
        self.mainWindow.action_New.setEnabled(state)
        '''
        if index == 0:
            self.mainWindow.actionEdit.setEnabled(False)
            self.mainWindow.actionDelete.setEnabled(False)
            self.mainWindow.action_New.setEnabled(False)
        else:
            self.mainWindow.actionEdit.setEnabled(True)
            self.mainWindow.actionDelete.setEnabled(True)
            self.mainWindow.actionDelete.setEnabled(True)
    '''
    def new_(self):
        d=NewEntity(self.auth,self.mainWindow)

    def delete_(self):
        d=DeleteDialog.DeleteDialog(self.auth)

    def about_(self):
        d=About()

    def logOut(self):
        self.mainWindow.application.setCurrentIndex(0)
        self.mainWindow.actionLogout.setEnabled(False)

    def loggedIn(self,index):
        if index > 0:
            self.mainWindow.actionLogout.setEnabled(True)
