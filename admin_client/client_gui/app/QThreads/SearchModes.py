from .. import clearGrid
from PyQt5.QtWidgets import QMainWindow,QCheckBox,QWidget
from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
from .GetProduct import GetProduct
from .UpdateSearchSelector import UpdateSearchSelector
from .. import clearGrid
class SearchModes(QThread):
    address="http://localhost:9000"
    w=None
    lock_search_mode=[]
    auth=None
    product=None
    ready=pyqtSignal(bool)
    def run(self):
        self.w.by_name.stateChanged.connect(self.state_change_name)
        self.w.by_upc.stateChanged.connect(self.state_changed_upc)
        self.w.by_homecode.stateChanged.connect(self.state_changed_homecode)
        self.w.by_id.stateChanged.connect(self.state_changed_id)
        self.w.Search.clicked.connect(self.search)
        
    def counted(self,state,objname):
        print(objname,state)
        if state == 2:
            self.lock_search_mode.append(objname)
        else:
            try:
                self.lock_search_mode.remove(objname)
            except Exception as e:
                print(e)

    def state_changed_upc(self,state):
        self.w.UPC.setEnabled(state)
        clearGrid(self,complete=False)
        self.counted(state,self.w.UPC.objectName())

    def state_change_name(self,state):
        self.w.search_name.setEnabled(state)
        clearGrid(self,complete=False)
        self.counted(state,self.w.search_name.objectName())

    def state_changed_homecode(self,state):
        self.w.homecode.setEnabled(state)
        clearGrid(self,complete=False)
        self.counted(state,self.w.homecode.objectName())

    def state_changed_id(self,state):
        self.w.ID.setEnabled(state)
        clearGrid(self,complete=False)
        self.counted(state,self.w.ID.objectName())

    
    def enable_buttons(self):
        self.ready.emit(True)
        self.w.Search.setEnabled(True)
        self.w.forwards_btn.setEnabled(True)
        if self.w.page.value() >= 1:
            self.w.back_btn.setEnabled(True)
        self.w.root.statusBar().clearMessage()
    def disable_buttons(self):
        self.w.Search.setEnabled(False)
        self.w.forwards_btn.setEnabled(False)
        self.w.back_btn.setEnabled(False)
        

    def search(self): 
        self.ready.emit(False)
        self.w.root.statusBar().showMessage("Searching...")
        self.w.root.stackedWidgetChange.emit(self.w.root.STACKED_INDEX.get("loading"))
        #self.disable_buttons() 
        try:
            self.product.terminate()
        except:
            pass
        clearGrid(self)
        if len(self.lock_search_mode) == 1 and 'ID' in self.lock_search_mode:
            print("getting 1 by id")
            self.product=GetProduct(address=self.address,auth=self.auth,mode="get",json=dict(ID=getattr(self.w,"ID").text()))
            self.product.w=self.w
            self.product.finished.connect(self.enable_buttons)
            self.product.start()
        else:
            json={}
            for mode in self.lock_search_mode:
                if mode == "homecode":
                    json["home_code"]=getattr(self.w,mode).text()
                elif mode == "ID":
                    json['id']=int(getattr(self.w,mode).text())
                elif mode == "UPC":
                    json['upc']=getattr(self.w,mode).text()
                elif mode == "search_name":
                    json['name']=getattr(self.w,mode).text()
                else:
                    json[mode]=getattr(self.w,mode).text()
            json['limit']=self.w.limit.value()
            json['page']=self.w.page.value()
            self.product=GetProduct(address=self.address,auth=self.auth,mode="post",json=json)
            self.product.w=self.w
            self.product.start()
            self.product.finished.connect(self.enable_buttons)
            #self.ready.emit(True)
            #self.product.finished.connect(self.UpdateSelectThread.start)
            #self.UpdateSelectThread.product=self.product.getResponse
        self.w.product_view.update() 
        self.w.root.stackedWidgetChange.emit(self.w.root.STACKED_INDEX.get("program"))           
        self.ready.emit(True)            
            #print(self.product.getResponse(),"3")
                        
