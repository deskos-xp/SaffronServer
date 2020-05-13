from PyQt5.QtWidgets import QMainWindow,QCheckBox,QWidget,QGridLayout
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QPushButton,QWidget,QPushButton,QSpacerItem,QSizePolicy
from PyQt5 import uic
from .QThreads.SearchModes import SearchModes
from .QThreads.DisplayDataDialog import DisplayDataDialog
from .QThreads.Deleter import Deleter
from . import clearGrid
class SearchViewGrid(QWidget):
    address:str=None
    auth:tuple=None
    need_buttons=pyqtSignal(dict)
    buttons=[]
    block=True
    #auto_search=pyqtSignal()

    def __init__(self,widget,auth,address):
        self.address=address
        self.auth=auth
        super(SearchViewGrid,self).__init__()
        self.w=widget
        self.search_modes=SearchModes()
        self.search_modes.w=widget
        self.search_modes.auth=self.auth
        self.search_modes.start()
        self.search_modes.ready.connect(self.setButtonStates)
    
        self.need_buttons.connect(self.add_buttons_preview)
        self.w.need_buttons=self.need_buttons
        self.w.page.valueChanged.connect(self.spinsChanged)
        self.w.limit.valueChanged.connect(self.spinsChanged)
        self.w.forwards_btn.clicked.connect(self.increment_page)
        self.w.back_btn.clicked.connect(self.decrement_page)
        #self.auto_search.connect(self.re_search)
   
    def setButtonStates(self,state):
        if self.w.page.value() > 0 and state == True:
            self.w.back_btn.setEnabled(state)
        else:
            self.w.back_btn.setEnabled(False)
        self.w.forwards_btn.setEnabled(state)
        self.w.Search.setEnabled(state)
        self.block=state
    
    def increment_page(self):      
        self.w.page.setValue(self.w.page.value()+1)
        if self.search_modes.ready == True:
            if self.w.page.value() > 0:
                if self.block == False:
                    self.w.back_btn.setEnabled(True)

    def decrement_page(self):
        v=self.w.page.value()
        if v > 0:
            self.w.page.setValue(v-1)
        if self.w.page.value() <= 0:
            self.w.back_btn.setEnabled(False)
    '''
    def re_search(self):
        self.search_modes.search()

    def search_emitter(self):
        self.auto_search.emit()
    '''
    def add_buttons_preview(self,data):
        
        print(data)
        if data != {}:
            displayDataDialog=DisplayDataDialog()
            
            displayDataDialog.w=self.w
            displayDataDialog.auth=self.auth
            displayDataDialog.address=self.address
            displayDataDialog.data=data 

            self.w.forwards_btn.setEnabled(True)
            widget=QWidget()
            uic.loadUi("app/forms/ProductSelector.ui",widget)
            widget.product_view_btn.setText(data.get("name"))
            widget.product_view_btn.clicked.connect(displayDataDialog.run)
            
            #deleter.finished.connect(self.search_emitter)
            
            self.w.product_view 
            if self.w.product_view.count() <= 0:
                self.w.product_view.addWidget(widget,0,0,1,1)
            else:
                print(self.w.product_view.count())
                self.w.product_view.addWidget(widget,self.w.product_view.count()+1,0,1,1)

            editor=None
            deleter=Deleter(widget,self.w,self.auth,self.address,data,"product",self.w.product_view.count())       
            widget.delete_btn.clicked.connect(deleter.start)
            
            #QGridLayout
            
            self.buttons.append(dict(button=widget,dialog=displayDataDialog,deleter=deleter,editor=editor))
            v=QSpacerItem(20, 40,QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.w.product_view.addItem(v,self.w.product_view.count()+1,0,1,1)
        else:
            clearGrid(self)
            for i in self.w.product_view.children():
                i.widget().deleteLater()
            #self.w.product_view.setItems([])
            self.w.forwards_btn.setEnabled(False)
    def spinsChanged(self):
        #QGridLayout.children()
        #print(self.sender())    
        clearGrid(self)
        self.buttons.clear()
        self.w.Search.click()
