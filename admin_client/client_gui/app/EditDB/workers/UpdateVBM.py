from PyQt5.QtCore import QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
import requests,os,sys,ast,json
from ...common.Fields import *

class UpdateVBMSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()


class UpdateVBM(QRunnable):
    def __init__(self,auth:dict,data:dict,identifier:int,name:str,mode=None):
        super(UpdateVBM,self).__init__()
        self.auth=auth
        self.data=data
        self.identifier=identifier
        self.name=name
        self.signals=UpdateVBMSignals()
        self.mode=mode
        self.old=dict(data)

    def run(self):
        self.data=stripStructures(self.data)
        print(self.data,self.identifier,self.name,self.mode)
        auth=(
            self.auth.get('username'),
            self.auth.get('password')
                )
        addrPOST="{server_address}/{name}/update/{ID}".format(
                **dict(
                    server_address=self.auth.get("server_address"),
                    name=self.name,
                    ID=self.data.get('id')
                    ))
        try:
            if self.mode == None:
                pass
            elif self.mode == Mode.GET:
                for m in ['remove','add']:
                    if m == 'remove':
                        if self.old.get('address') and len(self.old.get('address')) > 0:
                            old=self.old.get('address')[0].get('id')
                            addrGET="{addrPOST}/{mode}/address/{address_id}".format(**dict(addrPOST=addrPOST,address_id=old,mode=m))
                            response=self.signals.session.get(addrGET.format(m),auth=auth)
                            self.signals.hasResponse.emit(response)
                            print(addrGET)
                    else:
                        addrGET="{addrPOST}/{mode}/address/{address_id}".format(**dict(addrPOST=addrPOST,address_id=self.identifier.get('ID'),mode=m))
                        response=self.signals.session.get(addrGET.format(m),auth=auth)
                        self.signals.hasResponse.emit(response)
                        print(addrGET)
            elif self.mode == Mode.POST:
                self.data.__delitem__('id')
                print(addrPOST,self.data)
                response=self.signals.session.post(addrPOST,auth=auth,json=self.data)
                self.signals.hasResponse.emit(response)
            else:
                raise Exception("Invalid mode {mode}".format(**dict(mode=self.mode)))
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)
            self.signals.kill()
        self.signals.finished.emit()
