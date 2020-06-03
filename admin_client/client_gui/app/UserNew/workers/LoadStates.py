from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import json
from ...configs.config import config

class LoadStatesSignals(QObject):
    hasState:pyqtSignal=pyqtSignal(str)
    hasError:pyqtSignal=pyqtSignal(Exception)
    finished:pyqtSignal=pyqtSignal()
    killMe:bool=False

    @pyqtSlot()
    def kill(self):
        self.killMe=not self.killMe

class LoadStates(QRunnable):
    def __init__(self):
        super(LoadStates,self).__init__()
        self.signals=LoadStatesSignals()

    def run(self):
        try:
            with open(config.states.value,"r") as fd:
                while True:
                    stateInfo=json.load(fd)
                    for state in stateInfo:
                        self.signals.hasState.emit(state)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
