from PyQt5.QtCore import QThread,QCoreApplication,QObject
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import time,requests,sys

class ProductUpcImgUpdater(QThread):
    w=None
    parent=None
    auth=None
    address=None
    time=0.5
    path=None
    def run(self):
        app=QCoreApplication.instance()
        self.update_label()

    def upload(self):
        pass
        #do uploading here
    
    def update_label(self):
        if self.path != None:
            im:QLabel=self.w.product_upc_img
            im.setPixmap(QPixmap(self.path))
            lbl:QLabel=self.w.product_upc_img_lbl
            lbl.setText(self.path)
            while True:
                time.sleep(self.time)
                if lbl.text() != self.path:
                    lbl.setText(self.path)
                    im.setPixmap(QPixmap(self.path))
            
