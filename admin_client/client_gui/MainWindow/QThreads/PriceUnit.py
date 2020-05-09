from PyQt5.QtCore import QThread,QCoreApplication
import time,sys,requests
from ..tools.combobox_update import ComboBox_Update
from .Decor import Attempt
class PriceUnitThread(QThread,ComboBox_Update):
    w=None
    auth=None
    time=0.5
    address=None
    @Attempt
    def run(self):
        app=QCoreApplication.instance()
        if self.w != None and ((self.auth != ()) or (self.auth != None) or (len(self.auth) < 2)): 
            self.prunit_setup()
            while True:
                time.sleep(self.time)
                try:
                    self.prunit_setup()
                except Exception as e:
                    print(e)

    def prunit_setup(self):
        try:
            cb=self.w.price_unit
            if self.address == None:
                return
            status_response=requests.post("{}/priceUnit/get".format(self.address),auth=self.auth,json=dict(page=0,limit=sys.maxsize))
            if status_response.status_code != 200:
                return
            status=status_response.json()
            if 'objects' in status.keys():
                units=status['objects']
                units_names=[i['name'] for i in units]
                self.price_units=units
                #cb.addItems(units_names)
                self.needs_update(cb,units_names)
                cb.activated[str].connect(self.pu_onChange)
        except Exception as e:
            self.w.root.statusBar().showMessage(str(e))
            time.sleep(2)
            self.w.root.statusBar().clearMessage()
    def pu_onChange(self,text):
        pu=self.sender()
        print(text)


