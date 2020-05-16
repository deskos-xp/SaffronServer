import json,ast,os,sys,dotenv
from PyQt5.QtCore import QObject,QRunnable,pyqtSignal
'''
def getLocalizedPath(self):
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
'''
from .. import getLocalizedPath
class SaveAuthSignals(QObject):
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)

class SaveAuth(QRunnable):
    def __init__(self,auth:dict,credfile:str):
        self.path=getLocalizedPath()
        self.credfile=credfile
        self.signals=SaveAuthSignals()
        self.auth=auth
        super(SaveAuth,self).__init__()

    def run(self):
        try:
            with open(os.path.join(self.path[-1],self.credfile),"w") as fd:
                json.dump(self.auth,fd)
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
