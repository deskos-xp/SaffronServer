from PyQt5.QtCore import QAbstractListModel,Qt
import ast

class EditDBListModel(QAbstractListModel):
    def __init__(self,*args,items=None,mode):
        super(EditDBListModel,self).__init__()
        self.items=items or []
        self.mode=mode

    def data(self,index,role):
        #print(self.items[index.row()]) 
        if role == Qt.DisplayRole:
            text=self.items[index.row()]
            if self.mode != None and self.mode == 'address':
                textTMP="{id} - {street_number} {street_name}, {city}, {state} {ZIP} ({apartment_suite})".format(**text)
            else:
                try:
                    #print(text,type(text))
                    textTMP="{id} - {name}".format(**text)
                except:
                    textTMP="{NAME}".format(**dict(NAME=text))
            return textTMP
        
    def rowCount(self,index):
        return len(self.items)

