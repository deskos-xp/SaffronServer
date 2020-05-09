from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
from PyQt5.QtWidgets import QWidget
import os,json
from dotenv import load_dotenv
load_dotenv()
class StateComboBoxController(QThread):
    widget:QWidget=None
    newState=pyqtSignal(str)
    
    states=list()
    def read_config(self):
        conf=os.getenv("states_conf")
        with open(conf,"r") as c:
            self.states=json.load(c)

    def run(self):
        self.read_config()
        for k in self.states:
            self.newState.emit(k)
        self.finished.emit()
