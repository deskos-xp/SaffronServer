from PyQt5.QtCore import QCoreApplication,QThread,pyqtSignal
from PyQt5.QtWidgets import QDialog,QComboBox,QTextEdit,QLineEdit,QSpinBox
from .NewDepartment import NewDepartment
import string
class NewDepartmentDialogController(QDialog):
    auth:tuple=None
    address:str=None
    w=None
    widget=None
    json:dict=dict(name="",comment="",store_department_number=None)
    #addressID:int=None

    #jsonReady:pyqtSignal=pyqtSignal(dict,str)
    def __init__(self,widget,w,address,auth):
        self.widget=widget
        self.w=w
        super(NewDepartmentDialogController,self).__init__()
        self.auth=auth
        self.address=address
        widget.name.textChanged.connect(self.updateJson)
        widget.comment.textChanged.connect(self.updateJson)
        widget.store_department_number.valueChanged.connect(self.updateJson)
        widget.confirm.accepted.connect(self.accept)
        widget.confirm.rejected.connect(self.reject)
        widget.finished.connect(self.finished)
        self.newDepartmentThread=NewDepartment()
        self.newDepartmentThread.auth=auth
        self.newDepartmentThread.address=address
        self.newDepartmentThread.w=w 
        self.newDepartmentThread.widget=widget
        self.newDepartmentThread.departmentSent.connect(self.status_code_show)
        widget.setWindowTitle("New Department")
    def status_code_show(self,status_code):
        self.w.statusBar().showMessage(str(status_code))

    def finished(self,extra):
        print(extra)

    def accept(self):
        print(self.json)
        #send to server
        self.newDepartmentThread.json=self.json
        self.newDepartmentThread.start()
        self.widget.accept()

    def reject(self):
        #kill additional threads

        self.widget.reject()

    def updateJson(self):
        print(self.sender().objectName())
        if type(self.sender()) == type(QTextEdit()):
            self.json[self.sender().objectName()]=self.sender().toPlainText()
        elif type(self.sender()) == type(QLineEdit()):
            self.json[self.sender().objectName()]=self.sender().text()
        elif type(self.sender()) == type(QSpinBox()):
            self.json[self.sender().objectName()]=self.sender().value()
        print(self.json)
