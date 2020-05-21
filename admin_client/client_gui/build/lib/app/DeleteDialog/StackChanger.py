from PyQt5 import uic
from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal,QObject,QThreadPool,QModelIndex

from PyQt5.QtWidgets import QDialog,QComboBox,QWidget,QListWidgetItem,QListWidget,QStackedWidget

class StackChanger:
    enabledWidgetsChanger=[]
    def stack_changer(self,index:QModelIndex):
        self.dialog.views.setCurrentIndex(index.row())
        print(self.dialog.views.currentWidget().objectName())
        for i in self.enabledWidgetsChanger:
            i()

    def adrCH(self):
        try:
            self.adr.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def brandCH(self):
        try:
            self.brand.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def vendorCH(self):
        try:
            self.vendor.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def manufacturerCH(self):
        try:
            self.manufacturer.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def departmentCH(self):
        try:
            self.department.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def weightUnitCH(self):
        try:
            self.weightUnit.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def priceUnitCH(self):
        try:
            self.priceUnit.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def productCH(self):
        try:
            self.product.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def vendorCH(self):
        try:
            self.vendor.startWorker(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)


