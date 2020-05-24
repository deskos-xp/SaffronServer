#! /usr/bin/python3
from app.MainWindow import Main
from PyQt5.QtWidgets import QApplication
import sys
import faulthandler
#faulthandler.enable()
'''
class run:
    m=None
    def __init__(self):
        self.m=MainWindow


x=run()
x.m.main()
'''
sys._excepthook = sys.excepthook 
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1) 
sys.excepthook = exception_hook 
def main():
    #ecode=mainWindow.EXIT_CODE_REBOOT
    #while ecode == mainWindow.EXIT_CODE_REBOOT:
    ecode=0
    app = QApplication(sys.argv)
    ex=Main()
    ex.show()
    ecode=app.exec_()
    return ecode




if __name__ == "__main__":
    ecode=0
    while True:
        ecode=main()       
        if ecode != Main.EXIT_CODE_REBOOT:
            break
        print(ecode)
        del(ecode)
        ecode=0


