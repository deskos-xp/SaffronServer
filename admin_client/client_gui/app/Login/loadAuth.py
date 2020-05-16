import os,sys,json,ast
from .. import getLocalizedPath
from PyQt5.QtCore import QRunnable,QObject,pyqtSignal

class LoadAuthSignals(QObject):
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)

class LoadAuth(QRunnable):
    def __init__(self,widget,credfile):
        self.widget=widget
        self.credfile=credfile
        self.signals=LoadAuthSignals()
        super(LoadAuth,self).__init__()

    def run(self):
        try:
            with open(os.path.join(getLocalizedPath()[-1],self.credfile),"r") as fd:
                self.auth=json.load(fd)
                for k in self.auth.keys():
                    if self.auth.get(k) != None:
                        getattr(self.widget,k).setText(self.auth.get(k))
                        self.widget.rememberMe.setChecked(True)
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)


        self.signals.finished.emit()

