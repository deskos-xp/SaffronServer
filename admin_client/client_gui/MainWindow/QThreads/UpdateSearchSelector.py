from PyQt5.QtCore import QThread
from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

class UpdateSearchSelector(QThread):
    selectors={}
    product=None
    def __init__(self,**kwargs):
        super(UpdateSearchSelector,self).__init__()
        self.w=kwargs.get("w")

    def run(self):
        print(self.product,"selector ##")
        if self.product != None:
            status=self.product()
            if status != None:
                if status.get('object') != None:
                    print(status.get('object'))
                    self.w.need_buttons.emit(status.get('object'))
                elif status.get('objects') != None and status.get("objects") != []:
                    for p in status.get('objects'):
                        self.w.need_buttons.emit(p)
                    print(status.get('objects'))
