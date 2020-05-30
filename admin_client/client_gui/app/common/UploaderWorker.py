from PyQt5.QtCore import QObject,QThread,QRunnable,QThreadPool,pyqtSignal,pyqtSlot
import ast,json,requests,os,sys,enum

class UploaderWorkerSignals(QObject):
    killMe:bool=False
    session=requests.Session()
    uploaded:pyqtSignal=pyqtSignal(requests.Response,str)
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class UploaderWorkerEnum:
    TYPES=("upc_image","product_image")

class UploaderWorker(QRunnable):
    def __init__(self,auth:dict,WHAT:str,path:str,product_id:int):
        super(UploaderWorker,self).__init__()
        self.signals=UploaderWorkerSignals()
        self.auth=auth
        self.WHAT=WHAT
        self.path=path
        self.product_id=product_id

    def run(self):
        try:
            if self.WHAT not in UploaderWorkerEnum.TYPES:
                raise Exception("invalid WHAT as {WHAT}".format(**dict(WHAT=self.WHAT)))
            with open(self.path,"rb") as fd:
                files={
                        "file":fd
                        }
                response=self.signals.session.post(
                        "{address}/product/update/{product_id}/upload/{WHAT}".format(
                            **dict(address=self.auth.get("server_address"),product_id=self.product_id,WHAT=self.WHAT)
                            ),
                        json=dict(),
                        auth=(self.auth.get("username"),self.auth.get("password")),
                        files=files
                        )
                self.signals.uploaded.emit(response,self.WHAT)
        except Exception as e:
            self.signals.hasError.emit(e)
            print(e)

        self.signals.finished.emit()
