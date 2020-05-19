from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot,QAbstractItemModel,QAbstractTableModel
from PyQt5.QtWidgets import QTableView,QDialogButtonBox,QDialog,QWidget
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QColor,QPixmap

from .DataViewModel import DataViewModel
from .workers.GetImageFromServer import GetImageFromServer
from .workers.GetGeneratedBars import GetGeneratedUPC
class DataViewDialog(QDialog):
    def __init__(self,auth:dict,data:dict,widget:QWidget):
        self.data=data
        self.auth=auth
        self.dialog=QDialog(widget)
        super(DataViewDialog,self).__init__()
        uic.loadUi("app/DataView/forms/DataViewDialog.ui",self.dialog)
        print(self.data)
        self.model=DataViewModel(item=self.data,auth=self.auth)
        self.dialog.dataView.setModel(self.model)
         
        self.upcImgWorker=GetImageFromServer(self.auth,data.get("id"),"upc_image")
        self.upcImgWorker.signals.hasImage.connect(self.returnablePik)
        self.upcImgWorker.signals.hasError.connect(lambda x: print(x))
        self.qtp=QThreadPool.globalInstance()
        self.qtp.start(self.upcImgWorker)
        
        self.productImgWorker=GetImageFromServer(self.auth,data.get("id"),"product_image")
        self.productImgWorker.signals.hasImage.connect(self.returnablePik)
        self.productImgWorker.signals.hasError.connect(lambda x: print(x))
        self.qtp.start(self.productImgWorker)

        self.generatedUPCImgWorker=GetGeneratedUPC(self.auth,data.get("id"),"ean13","generated_upc")
        self.generatedUPCImgWorker.signals.hasImage.connect(self.returnablePik)
        self.generatedUPCImgWorker.signals.hasError.connect(lambda x: print(x))
        self.qtp.start(self.generatedUPCImgWorker)

        #self.dialog.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dialog.dataView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.dialog.dataView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)



        self.model.layoutChanged.emit()
        self.dialog.exec_()

    def returnablePik(self,piknic:QPixmap,whichImage:str):
        getattr(self.dialog,whichImage).setPixmap(piknic)
        print(piknic,whichImage)

