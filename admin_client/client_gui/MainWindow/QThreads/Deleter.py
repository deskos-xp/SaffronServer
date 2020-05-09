import requests,os,time,sys

from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
from PyQt5.QtWidgets import QGridLayout,QMainWindow

class Deleter(QThread):
    def __init__(self,widget,root_widget,auth,address,data,mode,pos):
        self.w=root_widget
        self.widget=widget
        self.auth=auth
        self.address=address
        self.data=data
        self.mode=mode
        self.status:requests.Response=None
        self.pos=pos
        super(Deleter,self).__init__()

    def run(self):
        self.w.root.stackedWidgetChange.emit(self.w.root.STACKED_INDEX.get('loading')) 
        if self.mode == "product":
            self.status=requests.delete("{address}/product/delete/{productId}".format(**dict(address=self.address,productId=self.data.get("id"))),auth=self.auth)
            print(self.status.json())
            print(self.data.get("id")) 
            self.w.product_view.removeWidget(self.widget)
            self.widget.deleteLater()
            self.w.product_view.update()
            #QGridLayout.removeWidget
        self.finished.emit()
        
        self.w.root.stackedWidgetChange.emit(self.w.root.STACKED_INDEX.get('program')) 
