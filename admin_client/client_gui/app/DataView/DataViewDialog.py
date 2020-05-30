from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot,QAbstractItemModel,QAbstractTableModel
from PyQt5.QtWidgets import QTableView,QDialogButtonBox,QDialog,QWidget
from PyQt5 import uic
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QColor,QPixmap

from..DataViewSmall.DataViewSmall import DataViewSmall

from .DataViewModel import DataViewModel
#from .workers.GetImageFromServer import GetImageFromServer
from ..common.GetImageFromServer import GetImageFromServer
from ..common.GetGeneratedBars import GetGeneratedUPC
import copy

#from .workers.GetGeneratedBars import GetGeneratedUPC
class DataViewDialog(QDialog):
    def __init__(self,auth:dict,data:dict,pkt:dict,widget:QWidget):
        self.data=data
        self.auth=auth
        self.dialog=QDialog(widget)
        super(DataViewDialog,self).__init__()
        uic.loadUi("app/DataView/forms/DataViewDialog.ui",self.dialog)
        #print(self.data)

        print("pkt_start",pkt.keys(),"pkt_end") 
        self.pkt=pkt
        #self.subD=dict()
        #for i in ['brand',"department","vendor","manufacturer"]:
        #    print(self.sub_datas.keys(),"*"*33,i)
        #    self.subD[i]=self.sub_datas.get(i)
        d={i:data.get(i) for i in data.keys() if i not in ['departments','addresses','vendors','brands','manufacturers']}
        self.model=DataViewModel(item=d,auth=self.auth)
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
        


        self.dialog.vendors.clicked.connect(self.nd)
        self.dialog.brands.clicked.connect(self.nd)
        self.dialog.manufacturers.clicked.connect(self.nd)
        self.dialog.departments.clicked.connect(self.nd)

        self.model.layoutChanged.emit()
        self.dialog.exec_()
        

    def nd(self):
        name=self.sender().objectName()
        #print(name,"$ name $"*20)
        #print(self.pkt[name][name],"$ {} $%".format(name))
        try:
            tmp=self.pkt[name][name]
            print(self.pkt.keys())
            #piece=self.subD.get(name)
            #print(piece.keys(),"$ piece $"*20)
            DataViewSmall(self.auth,tmp,self.dialog)
        except Exception as e:
            print(e)

    def returnablePik(self,piknic:QPixmap,whichImage:str):
        getattr(self.dialog,whichImage).setPixmap(piknic)
        #print(piknic,whichImage)

