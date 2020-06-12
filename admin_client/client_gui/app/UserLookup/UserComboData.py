from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget,QComboBox
from .workers.GetComboData import GetComboData

import requests,json,ast,sys
from ..common.Fields import *

class UserComboData:
    def __init__(self,auth,combo,model,view,parent,name):
        self.auth=auth
        self.name=name
        self.combo=combo
        self.parent=parent
        self.model=model
        self.view=view
        self.cache=[]
        if name in ['departments']:
            name=name[:-1]
            self.name=name
        self.worker=GetComboData(self.auth,self.name)
        def updateCombo(data):
            if data not in self.cache:
                self.cache.append(data)
            contained=[combo.itemText(i) for i in range(combo.count())]
            data['NAME']=self.name
            if self.name not in ['address']:
                dataStr="{id}:{NAME} - {name}".format(**data)
            else:
                dataStr=toAddressString(data)
            if dataStr not in contained:
                contained.append(dataStr)
                combo.clear()
                combo.addItems(contained)
        
        #print(model.item,'#%'*30)
        def updateModel(index):
            try:
                if index > 0:
                    self.model.load_data(self.cache[index])
            except Exception as e:
                print(e)

        self.combo.currentIndexChanged.connect(updateModel)

        self.worker.signals.hasItem.connect(updateCombo)
        self.worker.signals.hasError.connect(lambda x:print(x))
        self.worker.signals.hasResponse.connect(lambda x:print("{name} - {response}".format(**dict(name=self.name,response=x))))
        self.worker.signals.finished.connect(lambda: print("done getting {}".format(self.name)))
        QThreadPool.globalInstance().start(self.worker)
        def setComboIndex():
            contained=[combo.itemText(i) for i in range(combo.count())]
            matchFound=False
            for num,i in enumerate(contained):
                n=regexThisShit2(i)
                lid=self.model.item.get("id")
                if int(n.get('ID')) == lid:
                    self.combo.setCurrentIndex(num)
                    matchFound=True
                    break
            else:
                self.combo.setCurrentIndex(-1)
            if matchFound == False:
                self.combo.setCurrentIndex(-1)
        setComboIndex()
        
        print(model.item)
