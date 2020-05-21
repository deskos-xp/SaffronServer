from PyQt5.QtCore import QAbstractListModel,Qt

class DeleteDialogModel(QAbstractListModel):
    def __init__(self,*args,items=None,**kwargs):
        super(DeleteDialogModel,self).__init__()
        self.items=items or []

    def data(self,index,role):
        #print(self.items[index.row()]) 
        if role == Qt.DisplayRole:
            text=self.items[index.row()]
            textTMP="{NAME}".format(**dict(NAME=text))
            return textTMP
        
    def rowCount(self,index):
        return len(self.items)

