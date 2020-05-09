from PyQt5.QtCore import QThread,QCoreApplication
import requests,sys,time
from ..tools.combobox_update import ComboBox_Update
from .Decor import Attempt
class manufacturerThread(QThread,ComboBox_Update):
    time=0.5
    w=None
    auth=None
    address=None
    @Attempt
    def run(self):
        app=QCoreApplication.instance()
        if self.w != None and ((self.auth != ()) or (self.auth != None) or (len(self.auth) < 2)):
            self.manufacturer_setup()
        while True:
            time.sleep(self.time)
            try:
                self.manufacturer_setup()
            except Exception as e:
                print(e)
    
    def manufacturer_setup(self):
        try:
            cb=self.w.manufacturer_cb
            if self.address == None:
                return
            status_response=requests.post("{}/manufacturer/get".format(self.address),auth=self.auth,json=dict(page=0,limit=sys.maxsize))
            if status_response.status_code == 200:
                status=status_response.json()
                if 'objects' in status.keys():
                    units=status['objects']
                    units_names=[i['name'] for i in units]
                    self.manufacturers=units
                    #cb.addItems(units_names)
                    self.needs_update(cb,units_names)
                    cb.activated[str].connect(self.manufacturer_cb_onChange)
        except Exception as e:
            self.w.root.statusBar().showMessage(str(e))
            time.sleep(2)
            self.w.root.statusBar().clearMessage()
    def manufacturer_cb_onChange(self,text):
        cb=self.sender()
        print(text)


