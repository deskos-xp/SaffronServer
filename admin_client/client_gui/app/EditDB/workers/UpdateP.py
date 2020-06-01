from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json,ast,requests
from ...common.UploaderWorker import UploaderWorker

class UpdatePSignals(QObject):
    session=requests.Session()
    killMe:bool=False
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    finished:pyqtSignal=pyqtSignal()
    disabledGrid:pyqtSignal=pyqtSignal(bool)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class UpdateP(QRunnable):
    def __init__(self,auth:dict,base_item_data:dict,combos_data:dict,name:str,upc_image:dict,product_image:dict,old:dict):
        super(UpdateP,self).__init__()
        self.auth=auth
        self.base_item_data=base_item_data
        self.combos_data=combos_data
        self.old=old
        self.name=name
        self.upc_image=upc_image
        self.product_image=product_image
        self.signals=UpdatePSignals()
        self.auth_Tuple=(
            auth.get("username"),
            auth.get("password")
                )

    def updateBase(self):
        addr="{server_address}/{name}/update/{ID}".format(
            **dict(
                server_address=self.auth.get("server_address"),
                name=self.name,
                ID=self.base_item_data.get("id")
                )
                )
        bid=dict(self.base_item_data)
        print(addr)
        #only send changed data
        for k in self.old.keys():
            if self.old.get(k) == bid.get(k):
                try:
                    bid.__delitem__(k)
                except Exception as e:
                    print(e)
        response=self.signals.session.post(addr,auth=self.auth_Tuple,json=bid)
        self.signals.hasResponse.emit(response)

    def updateRelations(self):
        if self.signals.session == None:
            self.signals.session=requests.Session()
        print("update relations....")
        for i in self.combos_data.keys():
            #print(self.combos_data)
            for mode in ["remove","add"]:

                addr="{server_address}/{name}/update/{ID}/{mode}/{etype}/{item}"
                id_new=self.combos_data.get(i)
                id_old=self.old.get("{n}s".format(**dict(n=i)))
                if len(id_old) > 0:
                    id_old=id_old[0]
                    if int(id_new.get("ID")) != int(id_old.get('id')):
                        #remove old
                        #add new
                        if mode == "remove":
                            addrFormation=addr.format(**dict(
                                server_address=self.auth.get("server_address"),
                                name=self.name,
                                ID=self.base_item_data.get("id"),
                                mode=mode,
                                item=id_old.get("id"),
                                etype=i
                                ))
                        elif mode == "add":
                            addrFormation=addr.format(**dict(
                                server_address=self.auth.get("server_address"),
                                name=self.name,
                                ID=self.base_item_data.get("id"),
                                mode=mode,
                                item=id_new.get("ID"),
                                etype=i
                                ))
                        response=self.signals.session.get(addrFormation,auth=self.auth_Tuple)
                        self.signals.hasResponse.emit(response)
                else:
                    if id_new != None:
                        mode="add"
                        addrFormation=addr.format(**dict(
                                    server_address=self.auth.get("server_address"),
                                    name=self.name,
                                    ID=self.base_item_data.get("id"),
                                    mode=mode,
                                    item=id_new.get("ID"),
                                    etype=i
                                    ))
                        print(addrFormation)
                        response=self.signals.session.get(addrFormation,auth=self.auth_Tuple)
                        self.signals.hasResponse.emit(response)
        print("update relations")
    
    def updateImage(self):
        def hasResponse(code,string):
            self.signals.hasResponse.emit(code)
                #uploader_upc=
        
        productImage=self.product_image
        if productImage.get('name'):
            uploader_product=UploaderWorker(self.auth,"product_image",productImage.get('name'),self.base_item_data.get("id"))
            uploader_product.signals.hasError.connect(lambda e:print(e))
            uploader_product.signals.uploaded.connect(hasResponse)
            QThreadPool.globalInstance().start(uploader_product)

        #print(productImage)
        upcImage=self.upc_image
        #print(upcImage.get("name"),'z'*30)
        if upcImage.get("name"):
            #print('*'*60)
            uploader_upc=UploaderWorker(self.auth,"upc_image",upcImage.get('name'),self.base_item_data.get("id"))
            uploader_upc.signals.hasError.connect(lambda e:print(e))
            uploader_upc.signals.uploaded.connect(hasResponse)

            QThreadPool.globalInstance().start(uploader_upc)

    def run(self):
        self.signals.disabledGrid.emit(False)
        try:
            #print('s0')
            self.updateBase()
            #print('s1')
            self.updateRelations()
            #print('s2')
            self.updateImage()
            #print('s3')
        except Exception as e:
            #print("exception",e)
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
        self.signals.disabledGrid.emit(True)

