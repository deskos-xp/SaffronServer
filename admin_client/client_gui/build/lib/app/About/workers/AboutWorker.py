from PyQt5.QtCore import QThreadPool,QObject,QRunnable,pyqtSlot,pyqtSignal
import json,ast,os,sys
from PyQt5.QtGui import QPixmap,QImage
from io import BytesIO
x=__import__(__name__.split(".")[0])


class AboutWorkerSignals(QObject):
    hasData:pyqtSignal=pyqtSignal(dict)
    finished:pyqtSignal=pyqtSignal()
    killMe:bool=False
    hasError:pyqtSignal=pyqtSignal(Exception)    
    hasImage:pyqtSignal=pyqtSignal(QPixmap)

    @pyqtSlot()
    def kill(self):
        self.killMe=True

class AboutWorker(QRunnable):
    def __init__(self,config:str):
        super(AboutWorker,self).__init__()
        self.config=config
        self.signals=AboutWorkerSignals()

    def loadImage(self,name):
        data=x.Icons.getProgram_image(name)
        pix=QPixmap.fromImage(QImage.fromData(bytes(data.read())))
        self.signals.hasImage.emit(pix)
         
    def run(self):
        d=dict()
        try:
            with open(self.config,"r") as fd:
                d=json.load(fd)
            if 'icon' in d.keys():
                self.loadImage(d.get('icon'))
                d.__delitem__('icon')                

            self.signals.hasData.emit(d)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
