from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot,Qt
from PyQt5.QtWidgets import QDialog,QWidget,QItemDelegate,QComboBox,QCheckBox,QLineEdit,QPushButton

class ButtonDelegate(QItemDelegate):
        def __init__(self,parent,Callable,buttonName,data=None):
            QItemDelegate.__init__(self,parent)
            self.data=data or {}
            self.buttonName=buttonName or ""
            self.Callable=Callable

        def createEditor(self,parent,option,index):
            print("creating button!")
            button=QPushButton(parent)
            button.setText(self.buttonName)
            
            return button

        def setEditorData(self,editor,index):
            editor.blockSignals(True)
            editor.data=index.model().data(index)
            editor.clicked.connect(self.Callable)
            editor.blockSignals(False)
        
        def setModelData(self,editor,model,index):
            model.setData(index,editor.data,Qt.EditRole)
            #self.Callable()

        @pyqtSlot()
        def currentIndexChanged(self):
            self.commitData.emit(self.sender())

class LineEditDelegate(QItemDelegate):
    def __init__(self,parent,data=None):
        QItemDelegate.__init__(self,parent)
        self.data=data or []

    def createEditor(self,parent,option,index):
        combo = QLineEdit(parent)

        combo.addItems(','.join(self.data))

        return combo

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        ## do something
        print(index.model().data(index))
        editor.setText(','.join(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        model.setData(index,editor.text(),Qt.EditRole)

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class ComboBoxDelegate(QItemDelegate):
    def __init__(self,parent,data=None):
        QItemDelegate.__init__(self,parent)
        self.data=data or []

    def createEditor(self,parent,option,index):
        combo = QComboBox(parent)
        combo.clear()
        combo.addItems(self.data)

        return combo

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        ## do something
        print(index.model().data(index))
        editor.setCurrentText(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        model.setData(index,editor.currentText(),Qt.EditRole)

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())

class CheckBoxDelegate(QItemDelegate):
    def __init__(self,parent):
        QItemDelegate.__init__(self,parent)

    def createEditor(self,parent,option,index):
        combo = QCheckBox(parent)

        #boolean=['True','False']
        #combo.addItems(boolean)

        return combo

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        ## do something
        editor.setChecked(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        model.setData(index,editor.isChecked(),Qt.DisplayRole)

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())

