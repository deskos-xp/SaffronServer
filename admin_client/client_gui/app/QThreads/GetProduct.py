from PyQt5.QtCore import QCoreApplication,QThread
import sys,requests,json
from requests import Response
from .UpdateSearchSelector import UpdateSearchSelector


class GetProduct(QThread):
    VALID_MODES=["post","get"]
    address:str=None
    json:dict=None
    mode:str=None
    auth:tuple=None
    response=None
    w=None
    def __init__(self,**kwargs):
        super(GetProduct,self).__init__()
        self.address:str=kwargs.get("address")
        self.json:dict=kwargs.get("json")
        self.mode:str=kwargs.get("mode")
        self.auth:tuple=kwargs.get("auth")

    def getResponse(self):
        try:
            return self.response.json()
        except Exception as e:
            print(e)

    def get(self):
        try:
            if self.mode.lower() in self.VALID_MODES:
                if self.mode.lower() == "get":
                    self.response=requests.get("{}/product/get/{}".format(self.address,self.json.get("ID")),auth=self.auth)
                    #print(self.response.json())
                elif self.mode.lower() == "post":
                    print(self.json,"#json")
                    self.response=requests.post("{}/product/get".format(self.address),auth=self.auth,json=self.json)
                    print(self.response.json())
                else:
                    print("%s : not a valid mode!")
        except Exception as e:
            print(e)
        self.finished.emit()
        #print(self.mode)

    def run(self):
        try:
            self.UpdateSelectThread.terminate()
        except:
            pass
        self.get()
        self.UpdateSelectThread=UpdateSearchSelector(w=self.w)
        #self.product.finished.connect(self.UpdateSelectThread.start)
        self.UpdateSelectThread.product=self.getResponse
        self.UpdateSelectThread.start()
            

