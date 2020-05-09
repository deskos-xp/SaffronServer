from PyQt5.QtCore import QThread,QCoreApplication

class StyleSheet(QThread):
    def run(self):
        self.default_LineEdit=self.getDefaultLineEdit()
        self.warning_LineEdit=self.getWarningLineEdit()
        self.warning_SpinBox=self.getWarningSpinBox()
        self.default_SpinBox=self.getDefaultSpinBox()

    def getDefaultLineEdit(self):
        default_qlineedit="./Stylesheet/default_qlineedit.css"        
        with open(default_qlineedit,"rb") as i:
            dt=b""
            while True:
                d=i.read()
                if not d:
                    break
                dt+=d

        dt=str(dt,"utf-8")
        return dt

    def getWarningLineEdit(self):
        default_qlineedit="./Stylesheet/warning_qlineedit.css"        
        with open(default_qlineedit,"rb") as i:
            dt=b""
            while True:
                d=i.read()
                if not d:
                    break
                dt+=d

        dt=str(dt,"utf-8")
        return dt
    
    def getWarningSpinBox(self):
        default_qspinbox="./Stylesheet/warning_spinbox.css"        
        with open(default_qspinbox,"rb") as i:
            dt=b""
            while True:
                d=i.read()
                if not d:
                    break
                dt+=d

        dt=str(dt,"utf-8")
        return dt

    def getDefaultSpinBox(self):
        default_qspinbox="./Stylesheet/default_spinbox.css"        
        with open(default_qspinbox,"rb") as i:
            dt=b""
            while True:
                d=i.read()
                if not d:
                    break
                dt+=d

        dt=str(dt,"utf-8")
        return dt


