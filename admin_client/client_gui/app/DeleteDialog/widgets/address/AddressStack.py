from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal,QObject,QRunnable,QThread,QThreadPool,pyqtSlot
from PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QListWidget

import ast,requests,os,sys,json,time

from .worker import Worker
from .workerDel import WorkerDel
class AddressStack(QWidget):
    def __init__(self,parent:QWidget,designand:QWidget,dialog:QWidget,address:str,auth:tuple):
        self.w=parent
        self.address=address
        self.auth=auth
        self.widget=designand
        self.dialog=dialog
        super(AddressStack,self).__init__() 
        uic.loadUi("app/DeleteDialog/widgets/common/forms/common_stacks.ui",self.widget)
        self.widget.setObjectName("address")

        self.qtp=QThreadPool.globalInstance()
        self.worker=Worker(self.address,self.auth)
        self.worker.signals.ready.connect(self.updateSelector)
        #self.worker.signals.wait=self.widget.isVisible

        self.workerDel=WorkerDel(self.address,self.auth)
        self.workerDel.signals.done.connect(self.progressCounter)
        #self.workerDel.signals.wait=self.widget.isVisible

        dialog.rejected.connect(self.suicide)
        self.widget.confirm.rejected.connect(dialog.reject)
        #on accepted, do start self.workerDel

        #updates selector data
        self.qtp.start(self.worker)
        self.selector_items=[]

    @pyqtSlot(str)
    def isVisible(self,state):
        if state == "address":
            STATE=False
        else:
            STATE=True
        print(state,"fired as",STATE)
        self.workerDel.signals.wait(STATE)
        self.worker.signals.wait(STATE)

    @pyqtSlot()
    def suicide(self):
        self.worker.signals.kill()
        self.workerDel.signals.kill()

    def progressCounter(self,status_code:int):
        print(status_code)

    def updateSelector(self,data:dict):
        if data not in self.selector_items:
            self.selector_items.append(data)
            self.widget.selector.addItem(json.dumps(data))
        else:
            print("""not added as already present:\n {data}""".format(**dict(data=data)))
