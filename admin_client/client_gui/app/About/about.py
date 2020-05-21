from PyQt5.QtCore import QThreadPool,QObject,QRunnable,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QTableView,QHeaderView
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

from .AboutModel import AboutModel
from .workers.AboutWorker import AboutWorker
import os,sys,json,ast
top=__import__(__name__.split(".")[0])
top.getLocalizedPath()

class About(QDialog):
    def __init__(self):
        super(About,self).__init__()
        
        self.dialog=QDialog()
        uic.loadUi("app/About/forms/about.ui",self.dialog)
        
        self.path=top.getLocalizedPath()
        
        self.config="About/about.json"
        self.config=os.path.join(self.path[1],self.config)

        self.aboutWorker=AboutWorker(self.config)
        
        self.aboutWorker.signals.hasData.connect(self.change_dialog) 
        self.aboutWorker.signals.hasError.connect(lambda e:print(e,"#"))
        self.aboutWorker.signals.hasImage.connect(self.setImage)

        self.qtp=QThreadPool.globalInstance()
        self.qtp.start(self.aboutWorker)
         
        #print(self.config)

        self.dialog.exec_()

    @pyqtSlot(QPixmap)
    def setImage(self,image):
        self.dialog.image.setPixmap(image)

    @pyqtSlot(dict) 
    def change_dialog(self,data):
        #print(data,"stored")
        self.model=AboutModel(item=data)     
        self.dialog.aboutData.setModel(self.model)     
        self.dialog.aboutData.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dialog.aboutData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
