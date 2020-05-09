from PyQt5.QtCore import QThread,QCoreApplication,QObject
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import time,requests,sys

class ProductImgUpdater(QThread):
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
        #do upload here
 
    def update_label(self):
        if self.path != None:
            img:QLabel=self.w.product_img
            img.setPixmap(QPixmap(self.path))

            lbl:QLabel=self.w.product_img_lbl
            lbl.setText(self.path)
            while True:
                time.sleep(self.time)
                if lbl.text() != self.path:
                    lbl.setText(self.path)
                    img.setPixmap(QPixmap(self.path))

