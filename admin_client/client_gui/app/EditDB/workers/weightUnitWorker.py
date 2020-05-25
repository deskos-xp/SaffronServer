from PyQt5.QtCore import QRunnable,QObject,QCoreApplication,pyqtSlot,pyqtSignal,QThread
from dotenv import load_dotenv
import ast,json,os,sys
load_dotenv()

class WeightUnitWorkerSignals(QObject):
    finished:pyqtSignal=pyqtSignal()
    kill:bool=False
    hasUnit:pyqtSignal=pyqtSignal(str)
    hasError:pyqtSignal=pyqtSignal(Exception)

    @pyqtSlot()
    def killMe(self):
        self.kill=True


class WeightUnitWorker(QRunnable):
    def __init__(self):
        super(WeightUnitWorker,self).__init__()
        self.signals=WeightUnitWorkerSignals()
        self.config=os.getenv("weightUnits")

    def run(self):
        try:
            with open(self.config,"r") as fd:
                d=json.load(fd)
                if d:
                    for u in d:
                        self.signals.hasUnit.emit(u)
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
