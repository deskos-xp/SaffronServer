from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QHeaderView,QDialog,QComboBox,QPushButton,QWidget
import os,sys,ast,json,requests
from .EditDBTableModel import EditDBTableModel
from ..common.Fields import *
from .workers.SearchWorker import SearchWorker

class EditDB_Controller_P(QDialog):
    def __init__(self,auth:dict,parent,tab,data:dict,name:str):
        super(EditDB_Controller_P,self).__init__()
        self.auth=auth
        self.parent=parent
        self.tab=tab
        self.data=dict(data)
        self.name=name
        self.searchWorkers=dict()

        self.model=EditDBTableModel(item={})
        self.tab.editor.setModel(self.model)
        self.tab.editor.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab.editor.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.relations=['vendor','department','brand','manufacturer','address']
        self.old=dict(data)
        self.buttons()
        self.load_combos()

    def load_combos(self):
        for r in self.relations:
            print(r)
            if r in ['address']:
                plura="es"
            else:
                plura="s"
            combo=getattr(self.tab,"{name}{plural}".format(**dict(name=r,plural=plura)))
            self.load_combo(combo,r)

    def load_combo(self,combo,name):
        def updateCombo(data):
            contained=[combo.itemText(i) for i in range(combo.count())] 
            for l in data:
                if str(l) not in contained:
                    if name != "address":
                        combo.addItem("{id}:{name} - {NAME}".format(**dict(id=l.get("id"),name=name,NAME=l.get("name"))))
                    else:
                        combo.addItem(toAddressString(l))
            combo.lineEdit().setReadOnly(True)
        self.searchWorkers[name]=SearchWorker(self.auth,dict(page=0,limit=sys.maxsize),name,fields(name))
        self.searchWorkers[name].signals.hasError.connect(lambda e:print(e))
        #self.searchWorkers[name].signals.hasItem.connect(updateCombo)
        self.searchWorkers[name].signals.hasItems.connect(updateCombo)
        self.searchWorkers[name].signals.finished.connect(lambda :print("finished!"))

        QThreadPool.globalInstance().start(self.searchWorkers[name])
    def buttons(self):
        self.tab.clear.clicked.connect(self.clear_)

    @pyqtSlot(bool)
    def clear_(self,state):
        if self.old:
            self.model.load_data(stripStructures(self.old,delFields=["product_image","upc_image"]))
        else:
            self.model.load_data(stripStructures(fields(self.name),delFields=["product_image","upc_image"]))
        self.model.layoutChanged.emit()
        plura="s"
        for r in self.relations:
            print(r)
            if r in ['address']:
                plura="es"
            else:
                plura="s"
            getattr(self.tab,"{name}{plural}".format(**dict(name=r,plural=plura))).setCurrentIndex(-1) 
