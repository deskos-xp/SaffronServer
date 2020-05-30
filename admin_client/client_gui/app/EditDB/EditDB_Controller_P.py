from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QHeaderView,QDialog,QComboBox,QPushButton,QWidget
from PyQt5.QtGui import QPixmap
import os,sys,ast,json,requests
from .EditDBTableModel import EditDBTableModel
from ..common.Fields import *
from ..common.GetImageFromServer import GetImageFromServer
from ..common.FS import *
from .workers.SearchWorker import SearchWorker

class EditDB_Controller_P(QDialog):
    wantsToSwitch:pyqtSignal=pyqtSignal(dict)
    def __init__(self,auth:dict,parent,tab,data:dict,name:str):
        super(EditDB_Controller_P,self).__init__()
        self.upc_image=QPixmap()
        self.product_image=QPixmap()

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
        self.relations=['vendor','department','brand','manufacturer']
        self.old=dict(data)
        self.buttons()
        self.load_combos()

    def load_combos(self):
        for r in self.relations:
            #print(r)
            if r in ['address']:
                plura="es"
            else:
                plura="s"
            combo=getattr(self.tab,"{name}{plural}".format(**dict(name=r,plural=plura)))
            self.load_combo(combo,r)

    def setCombos_(self):
        for i in self.relations:
            if i in ['address']:
                plura="es"
            else:
                plura="s"
            plural="{name}{plural}".format(**dict(name=i,plural=plura))
            combo=getattr(self.tab,plural)
            self.setCombos(combo,self.data.get(plural))


    def setCombos(self,combo,data):
        #print(data,'8'*8)
        if type(data) == type(list()):
            if len(data) > 0:
                data=data[0]
        if data in [None,{},[]]:
            combo.setCurrentIndex(-1)
        else:
            print("combo count {count}".format(**dict(count=combo.count())))
            for i in range(combo.count()):
                ss=regexThisShit2(combo.itemText(i))
                if ss != None:
                    if int(ss.get('ID')) == data.get('id'):
                        print(ss,'b'*40)
                        combo.setCurrentIndex(i)
                        return
                    else:
                        combo.setCurrentIndex(-1)
            else:
                combo.setCurrentIndex(-1)

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
            self.setCombos(combo,data)
        self.searchWorkers[name]=SearchWorker(self.auth,dict(page=0,limit=sys.maxsize),name,fields(name))
        self.searchWorkers[name].signals.hasError.connect(lambda e:print(e))
        #self.searchWorkers[name].signals.hasItem.connect(updateCombo)
        self.searchWorkers[name].signals.hasItems.connect(updateCombo)
        self.searchWorkers[name].signals.finished.connect(lambda :print("finished!"))

        QThreadPool.globalInstance().start(self.searchWorkers[name])

    @pyqtSlot(QPixmap,str)
    def setImages(self,pixm,name,backup=True):
        #self.tab.product_image.setPixmap(pixm)
        getattr(self.tab,name).setPixmap(pixm)
        if backup == True:
            self.__dict__[name]=pixm

    def restoreImages(self):
        self.tab.upc_image.setPixmap(self.upc_image)
        self.tab.product_image.setPixmap(self.product_image)

    def getImages(self):
        getImage=GetImageFromServer(self.auth,self.data.get("id"),"product_image")
        getupc=GetImageFromServer(self.auth,self.data.get("id"),"upc_image")
        
        getImage.signals.hasImage.connect(self.setImages)
        getImage.signals.hasError.connect(lambda e:print(e))
        getImage.signals.hasBlankPixmap.connect(self.setImages)

        getupc.signals.hasImage.connect(self.setImages)
        getupc.signals.hasError.connect(lambda e:print(e))
        getupc.signals.hasBlankPixmap.connect(self.setImages)

        QThreadPool.globalInstance().start(getImage)
        QThreadPool.globalInstance().start(getupc)

    def edit_sub(self):
        name=self.sender().objectName()
        dname=name.replace("_edit","")
        combo=getattr(self.tab,dname+"s")
        identifiers=regexThisShit2(combo.currentText())
        if identifiers:
            self.wantsToSwitch.emit(identifiers)

    @pyqtSlot()
    def get_new_image(self):
        name=self.sender().objectName().replace("new_","")
        path=getFilePathDialog("Get {name}".format(**dict(name=name.replace("_"," "))))
        pixm=pathToQPixmap(path)
        if type(pixm) == type(QPixmap()):
            getattr(self.tab,name).setPixmap(pixm)
        else:
            getattr(self.tab,name).setPixmap(QPixmap())

    def buttons(self):
        self.tab.clear.clicked.connect(self.clear_)
        self.tab.vendor_edit.clicked.connect(self.edit_sub)
        self.tab.brand_edit.clicked.connect(self.edit_sub)
        self.tab.manufacturer_edit.clicked.connect(self.edit_sub)
        self.tab.department_edit.clicked.connect(self.edit_sub)
        self.tab.new_product_image.clicked.connect(self.get_new_image)
        self.tab.new_upc_image.clicked.connect(self.get_new_image)

    @pyqtSlot(bool)
    def clear_(self,state):
        self.restoreImages()
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
            if self.data:
                pass
            else:
                getattr(self.tab,"{name}{plural}".format(**dict(name=r,plural=plura))).setCurrentIndex(-1) 
        self.setCombos_()
