from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal,QObject,QRunnable,QThread,QThreadPool,pyqtSlot
from PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QListWidget,QComboBox

import ast,requests,os,sys,json,time

from .worker import Worker
from .workerDel import WorkerDel
class AddressStack(QWidget):
    done_del:pyqtSignal=pyqtSignal()
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
        #self.setupDelWorker()
        #self.workerDel.signals.wait=self.widget.isVisible

        dialog.rejected.connect(self.suicide)
        self.widget.confirm.rejected.connect(dialog.reject)
        #on accepted, do start self.workerDel

        #updates selector data
        self.qtp.start(self.worker)
        self.selector_items=[]
        

        self.widget.selector.textActivated.connect(self.update_viewer)
        self.widget.confirm.accepted.connect(self.startDelWorker) 


    def setupDelWorker(self):
        self.workerDel=WorkerDel(self.address,self.auth)
        self.workerDel.signals.done.connect(self.progressCounter)

    def startDelWorker(self):
        text=self.widget.selector.currentText().replace("null","None")
        if text and 'id' in ast.literal_eval(text).keys():
            self.setupDelWorker()

            ID=ast.literal_eval(text).get("id")
            self.workerDel.signals.setID(ID)
            self.qtp.start(self.workerDel)
                    
    def update_viewer(self,data):
        self.widget.tableWidget.clearContents()
        self.widget.tableWidget.setRowCount(0)

        print(data,"---<*>")
        data=data.replace("null","None")
        
        #addr=self.widget.selector.currentText(data)
        structure=ast.literal_eval(data)
        for num,key in enumerate(structure.keys()):
            print(num,key)
            self.widget.tableWidget.insertRow(num)
            self.widget.tableWidget.setItem(num,0,QTableWidgetItem(key))
            self.widget.tableWidget.setItem(num,1,QTableWidgetItem(str(structure[key])))
        self.widget.tableWidget.resizeRowsToContents()
        self.widget.tableWidget.resizeColumnsToContents()

    @pyqtSlot(str)
    def isVisible(self,state):
        if state == "address":
            STATE=False
        else:
            STATE=True
        print(state,"fired as",STATE)
        try:
            self.workerDel.signals.wait(STATE)
        except Exception as e:
            print(e)
        self.worker.signals.wait(STATE)

    @pyqtSlot()
    def suicide(self):
        self.worker.signals.kill()
        try:
            self.workerDel.signals.kill()
        except Exception as e:
            print(e)

    def progressCounter(self,status_code:int,ID:int):
        print(status_code)
        self.done_del.emit()
        self.dialog.accept()
        self.widget.selector.clear()

    def updateSelector(self,data:dict):
        if data not in self.selector_items:
            self.selector_items.append(data)
            self.widget.selector.addItem(json.dumps(data))
        else:
            print("""not added as already present:\n {data}""".format(**dict(data=data)))
