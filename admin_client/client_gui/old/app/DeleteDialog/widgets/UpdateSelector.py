from PyQt5.QtCore import QThread,QObject,QRunnable,pyqtSignal
import os,sys
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import QListWidget,QListWidgetItem
class UpdateSelectorSignals(QObject):
    #def __init__(self):
    #    super(UpdateSelectorSignals,self).__init__()
    ready:pyqtSignal=pyqtSignal(list)

class UpdateSelector(QRunnable):
    items=["address","brand","vendor","manufacturer","department","weightUnit","priceUnit","product"]
    #done=pyqtSignal(QStandardItemModel)
    def __init__(self,parent,widget):
        super(UpdateSelector,self).__init__()
        #self.w=parent
        #self.widget=widget
        self.signals=UpdateSelectorSignals()

    def run(self):
        #self.model=QStandardItemModel()
        #for i in self.items:
        #    self.model.appendRow(QStandardItem(i))
        
        self.signals.ready.emit(self.items)
        #self.widget.setModel(self.model)
        
