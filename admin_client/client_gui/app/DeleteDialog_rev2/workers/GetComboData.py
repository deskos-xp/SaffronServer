from PyQt5.QtCore import QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
import ast,requests,os,sys

class GetComboDataSignals(QObject):
    killMe:bool=False
    hasItems:pyqtSignal=pyqtSignal(dict,str)
    hasError:pyqtSignal=pyqtSignal(Exception)    
    finish:pyqtSignal=pyqtSignal()
    session:requests.Session=requests.Session()
    
    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class GetComboData(QRunnable):
    def __init__(self,auth:dict,name:str):
        super(GetComboData,self).__init__()
        self.signals=GetComboDataSignals()
        self.auth=auth
        self.name=name

    def run(self):
        try:
            address="{address}/{name}/get".format(**dict(address=self.auth['server_address'],name=self.name))
            postable=dict(limit=sys.maxsize,page=0)
            session=self.signals.session.post(address,json=postable,auth=(self.auth.get("username"),self.auth.get("password")))
            if session.status_code == 200:
                if 'status' in session.json().keys():
                    d=session.json().get(session.json().get('status'))
                    for i in d:
                        if self.name == "address":
                            i['name']="{street_number} {street_name}, {city}, {state} {ZIP}".format(**i)
                        self.signals.hasItems.emit(i,self.name)
            print(address)
            #self.signals.session.post()
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)
        self.signals.finish.emit()            
