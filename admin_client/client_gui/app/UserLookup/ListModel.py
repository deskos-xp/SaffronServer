from PyQt5.QtCore import QAbstractListModel,Qt

class ListModel(QAbstractListModel):
    def __init__(self,*args,TYPE=None,items=None,**kwargs):
        super(ListModel,self).__init__()
        self.items=items or []
        self.TYPE=TYPE

    def data(self,index,role):
        if role == Qt.DisplayRole:
            text=self.items[index.row()]
            textTMP="{ID}:{TYPE} - {NAME} [{lname},{mname},{fname}]".format(**dict(TYPE=self.TYPE,ID=text.get("id"),NAME=text.get("uname"),lname=text.get('lname'),fname=text.get('fname'),mname=text.get('mname')))
            return textTMP

    def rowCount(self,index):
        return len(self.items)

