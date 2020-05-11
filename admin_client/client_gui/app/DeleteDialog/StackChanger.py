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
            self.adr.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def brandCH(self):
        try:
            self.brand.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def vendorCH(self):
        try:
            self.vendor.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def manufacturerCH(self):
        try:
            self.manufacturer.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def departmentCH(self):
        try:
            self.department.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def weightUnitCH(self):
        try:
            self.weightUnit.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def priceUnitCH(self):
        try:
            self.priceUnit.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def productCH(self):
        try:
            self.product.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)

    def vendorCH(self):
        try:
            self.vendor.isVisible(self.dialog.views.currentWidget().objectName())
        except Exception as e:
            print(e)


