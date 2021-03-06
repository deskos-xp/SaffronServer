from PyQt5.QtCore import QAbstractListModel,Qt

class ListModel(QAbstractListModel):
    def __init__(self,*args,items=None,**kwargs):
        super(ListModel,self).__init__()
        self.items=items or []

    def data(self,index,role):
        if role == Qt.DisplayRole:
            text=self.items[index.row()]
            textTMP="{ID} - {NAME}".format(**dict(ID=text.get("id"),NAME=text.get("name")))
            return textTMP

    def rowCount(self,index):
        return len(self.items)

