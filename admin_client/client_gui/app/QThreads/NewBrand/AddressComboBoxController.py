from PyQt5.QtCore import QThread,QCoreApplication,pyqtSignal
from PyQt5.QtWidgets import QWidget
import os,json,requests,time
from dotenv import load_dotenv
load_dotenv()
class AddressComboBoxController(QThread):
    TIME=0.5
    widget:QWidget=None
    newAddress=pyqtSignal(str)
    address:str=None
    auth:tuple=None
    addrs=list()
    status:requests.Response=None

    def get_address(self):
        print("get_address()")
        try:
            self.status=requests.post("{address}/address/get".format(**dict(address=self.address)),json=dict(),auth=self.auth)
            #try stream option later
            print(self.status.status_code) 
        except Exception as e:
            print(e)
            #self.widget.root.statusBar().showMessage(str(e))
        print(self.status) 


    def run(self):
        while True:
            self.get_address()
            if self.status != None:
                try:
                    stat=self.status.json()
                    if stat != None:
                        addrs=stat.get("objects")
                        for i in addrs:
                            if i['apartment_suite'] == None or i['apartment_suite'] == "":                            
                                self.newAddress.emit("{id} : {street_number} {street_name},{city}, {state}{ZIP}".format(**i))
                            else:
                                self.newAddress.emit("{id} : {street_number} {street_name},{city}, {state}{ZIP} APT - {apartment_suite}".format(**i))

                    time.sleep(self.TIME)
                except Exception as e:
                    print(e)
            else:
                break
        self.finished.emit()
