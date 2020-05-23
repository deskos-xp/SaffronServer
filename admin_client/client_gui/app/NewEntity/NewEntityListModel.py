from PyQt5.QtCore import QAbstractListModel,Qt

class NewEntityListModel(QAbstractListModel):
    def __init__(self,*args,items=None,**kwargs):
        super(NewEntityListModel,self).__init__()
        self.items= items or []

    def data(self,index,role):
        if role == Qt.DisplayRole:
            text=self.items[index.row()]
            return text

    def rowCount(self,index):
        return len(self.items)
