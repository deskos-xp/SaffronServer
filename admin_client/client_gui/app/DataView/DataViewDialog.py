from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot,QAbstractItemModel,QAbstractTableModel
from PyQt5.QtWidgets import QTableView,QDialogButtonBox,QDialog,QWidget
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView

from .DataViewModel import DataViewModel

class DataViewDialog(QDialog):
    def __init__(self,auth:dict,data:dict,widget:QWidget):
        self.data=data
        self.auth=auth
        self.dialog=QDialog(widget)
        super(DataViewDialog,self).__init__()
        uic.loadUi("app/DataView/forms/DataViewDialog.ui",self.dialog)
        print(self.data)
        self.model=DataViewModel(item=self.data)
        self.dialog.dataView.setModel(self.model)
        

        #self.dialog.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dialog.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.dialog.dataView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)



        self.model.layoutChanged.emit()
        self.dialog.exec_()

