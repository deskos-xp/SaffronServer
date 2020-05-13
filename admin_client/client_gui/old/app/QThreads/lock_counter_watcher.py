from PyQt5.QtCore import QThread,QCoreApplication
import time 

class Watcher(QThread):
    parent=None
    TIME=0.5
    w=None
    unlock_len=6
    lock_counter={}
    print_check=None
    def __init__(self,print_check:bool=False,**kwargs):
        super(QThread,self).__init__()
        self.parent=kwargs.get("parent")
        self.TIME=kwargs.get("TIME")
        self.w=kwargs.get("w")
        self.unlock_len=kwargs.get("unlock_len")
        self.print_check=print_check
    def run(self):
        if self.parent != None:
            while True:
                try:
                    if self.print_check == True:
                        print(self.lock_counter.keys())
                    if len(self.lock_counter.keys()) == self.unlock_len:
                        self.w.save_product_info.setEnabled(True)
                    else:
                        self.w.save_product_info.setEnabled(False)
                except Exception as e:
                    print(e)
                time.sleep(self.TIME)
