from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal,QObject,QRunnable,QThread,QThreadPool,pyqtSlot
from PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QListWidget,QComboBox

import ast,requests,os,sys,json,time,inspect

from .worker import Worker
from .workerDel import WorkerDel
from dotenv import load_dotenv
load_dotenv()
class EntityStack(QWidget):
    done_del:pyqtSignal=pyqtSignal()
    def __init__(self,parent:QWidget,designand:QWidget,dialog:QWidget,address:str,auth:tuple,objectName:str):
        self.w=parent
        self.address=address
        self.auth=auth
        self.widget=designand
        self.dialog=dialog
        
        super(EntityStack,self).__init__() 
        #need a way to get local forms dir for here
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        self.form=os.path.join(os.path.join(path,os.getenv("form_dir")),os.getenv("form")) 
        #exit(1)
        uic.loadUi(self.form,self.widget)

        self.widget.setObjectName(objectName)
        self.setObjectName(objectName+"_controller")
        
        self.qtp=QThreadPool.globalInstance()
        
        self.worker=Worker(self.auth,self.address,self.widget.objectName())
        self.worker.signals.ready.connect(self.updateSelector)
        

        dialog.rejected.connect(self.suicide)
        self.widget.confirm.rejected.connect(self.suicide)
        #on accepted, do start self.workerDel

        #updates selector data
        self.qtp.setExpiryTimeout(15000)
        self.qtp.start(self.worker)
        self.selector_items=[]
        

        self.widget.selector.textActivated.connect(self.update_viewer)
        self.widget.confirm.accepted.connect(self.startDelWorker) 


    def setupDelWorker(self):
        self.workerDel=WorkerDel(self.auth,self.address,self.widget.objectName())
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
        if state == self.widget.objectName():
            STATE=False
        else:
            STATE=True

        print(STATE,"fired as",state)
        if STATE == False:
            self.suicide_noclose()
        else:
            self.worker=Worker(self.auth,self.address,self.widget.objectName())
            self.worker.signals.ready.connect(self.updateSelector)
            self.qtp.start(self.worker)

    def suicide_noclose(self):
        print("suicide triggered!")
        self.worker.signals.kill()
        try:
            self.workerDel.signals.kill()
        except Exception as e:
            print(e)

    @pyqtSlot()
    def suicide(self):
        self.worker.signals.kill()
        try:
            self.workerDel.signals.kill()
        except Exception as e:
            print(e)
        self.dialog.close()

    def progressCounter(self,status_code:int,ID:int):
        print(status_code)
        self.done_del.emit()
        self.suicide()
        self.widget.selector.clear()

    def updateSelector(self,data:dict):
        if data not in self.selector_items:
            self.selector_items.append(data)
            self.widget.selector.addItem(json.dumps(data))
        else:
            print("""not added as already present:\n {data}""".format(**dict(data=data)))
