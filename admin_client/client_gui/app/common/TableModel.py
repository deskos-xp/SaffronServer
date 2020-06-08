from PyQt5.QtCore import QAbstractTableModel,Qt,QModelIndex,QThreadPool
from PyQt5.QtGui import QColor
class TableModel(QAbstractTableModel):
    def __init__(self,*args,item=None,**kwargs):
        super(TableModel,self).__init__()
        self.item=item or {}
        self.items=[[i,self.item.get(i)] for i in self.item.keys()]
        #print(item)
        self.load_data(self.items)
        self.DEFAULT_ALIGNMENT=[Qt.AlignLeft,Qt.AlignCenter]
        self.auth=kwargs.get('auth')
       
    def load_data(self, data):
        print(data,'#'*30)
        skip=False
        if type(data) == type(dict()):
            self.item=data
            tmp=[[i,data.get(i)] for i in data.keys() if i != 'address']
            #tmp.append(['address',str(data.get('address'))])
            data=tmp
        
        elif isinstance(data,list):
            print(data,'list'*20)
            if len(data) > 0:
                if isinstance(data[0],dict):
                    data=data[0]
                    self.item=data
                    tmp=[[i,data.get(i)] for i in data.keys() if i != 'address']
                    data=tmp
                    
        if len(data) > 0:
            print(data,'?'*100)
            self.fields = [i[0] for i in data]    
            self.vals = [i[1] for i in data]
        else:
            self.vals=[]
        self.column_count = 2
        self.row_count = len(self.vals)
        self.layoutChanged.emit()

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Fields", "Values")[section]
        else:
            return "{}".format(section)

    '''
    def flags(self,index):
        baseflags=QAbstractTableModel.flags(self,index)
        if index.column() == 1:
            return baseflags | Qt.ItemIsEditable
        else:
            return baseflags
    '''

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
         
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
