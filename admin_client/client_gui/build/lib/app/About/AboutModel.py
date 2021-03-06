from PyQt5.QtCore import QAbstractTableModel,Qt,QModelIndex,QThreadPool
from PyQt5.QtGui import QColor

class AboutModel(QAbstractTableModel):
    def __init__(self,*args,item=None,**kwargs):
        super(AboutModel,self).__init__()
        self.item=item or {}
        self.items=[[i,self.item.get(i)] for i in self.item.keys()]
        self.load_data(self.items)
        self.DEFAULT_ALIGNMENT=[Qt.AlignLeft,Qt.AlignCenter]
        #print(self.items)   

    def reload_data(self,data:dict):
        items=[[i,data.get(i)] for i in data.keys()]
        self.items=items
        self.load_data(items)
 
    def load_data(self,data:list):
        self.fields=[i[0] for i in data]
        self.vals=[i[1] for i in data]
        self.column_count=2
        self.row_count=len(self.vals)

    def rowCount(self,parent=QModelIndex()):
        return self.row_count;

    def columnCount(self,parent=QModelIndex()):
        return self.column_count

    def headerData(self,section,orientation,role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Fields","Values")[section]
        else:
            return "{}".format(section)

    def data(self,index,role=Qt.DisplayRole):
        column=index.column()
        row=index.row()
        if role == Qt.DisplayRole:
            if column == 0: 
                return self.fields[row]
            elif column == 1:
                return self.vals[row]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return self.DEFAULT_ALIGNMENT[column]

        return None
