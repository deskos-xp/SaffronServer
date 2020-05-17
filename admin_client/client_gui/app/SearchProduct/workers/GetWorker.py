import os,sys,requests,json,ast
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from .. import SearchModeEnum

class GetWorkerSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasItem:pyqtSignal=pyqtSignal(object)
    hasError:pyqtSignal=pyqtSignal(Exception)
    session=requests.Session()

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()


class GetWorker(QRunnable):
    def __init__(self,auth:dict,data:dict,URI:str,mode):
        self.auth=auth
        self.data=data
        self.URI=URI
        self.signals=GetWorkerSignals()
        self.mode=mode
        super(GetWorker,self).__init__()

    def run(self):
        try:
            response:requests.Response=None
            if self.mode == SearchModeEnum.GET:
                response=self.signals.session.get(self.URI,auth=(self.auth.get("username"),self.auth.get("password")))
            elif self.mode == SearchModeEnum.POST:
                response=self.signals.session.post(self.URI,auth=(self.auth.get("username"),self.auth.get("password")),json=self.data)
            else:
                raise Exception("invalid mode {mode}".format(self.mode))
            if response != None:
                if response.status_code == 200:
                    j=response.json()
                    if 'object' in j.keys() and j.get('object') not in [None,[],{}]:
                        print(j.get('object'))
                        self.signals.hasItem.emit(j.get('object'))
                    elif 'objects' in j.keys() and j.get('objects') not in [None,[]]:
                        for i in j.get('objects'):
                            self.signals.hasItem.emit(i)
                        print(j.get('objects'))
                    else:
                        self.signals.hasError.emit(Exception("no results!"))
                else:
                    self.signals.hasError.emit(Exception(str(response.status_code)))
            else:
                self.signals.hasError.emit(Exception("response var was None"))
            #do something
        except Exception as e:
            self.signals.hasError.emit(e)
            print(e)
        self.signals.finished.emit()
