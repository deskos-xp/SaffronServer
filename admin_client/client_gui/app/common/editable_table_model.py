from PyQt5.QtCore import QAbstractTableModel,Qt,QModelIndex,QThreadPool
from PyQt5.QtGui import QColor
import enum
class editable_table_enum(enum.Enum):
    EDITABLE_ID=True
    NON_EDITABLE_ID=True

class editable_table_model(QAbstractTableModel):
    def __init__(self,*args,item=None,**kwargs):
        super(editable_table_model,self).__init__()
        self.item=item or {}
        self.items=[[i,self.item.get(i)] for i in self.item.keys()]
        #print(item)
        self.load_data(self.items)
        self.DEFAULT_ALIGNMENT=[Qt.AlignLeft,Qt.AlignCenter]
        self.auth=kwargs.get('auth')
        self.ID_MODE=kwargs.get("ID_MODE")
        if self.ID_MODE == None:
            self.ID_MODE=editable_table_enum.EDITABLE_ID

    def load_data(self, data):
        #print(data,'#'*30)
        skip=False
        if type(data) == type(dict()):
            self.item=data
            tmp=[[i,data.get(i)] for i in data.keys() if i != 'address']
            #tmp.append(['address',str(data.get('address'))])
            data=tmp
        
        elif isinstance(data,list):
            #print(data,'list'*20)
            if len(data) > 0:
                if isinstance(data[0],dict):
                    data=data[0]
                    self.item=data
                    tmp=[[i,data.get(i)] for i in data.keys() if i != 'address']
                    data=tmp
                    
        if len(data) > 0:
            #print(data,'?'*100)
            self.fields = [i[0] for i in data]    
            self.vals = [i[1] for i in data]
        else:
            self.vals=[]
        self.column_count = 2
        self.row_count = len(self.vals)
        self.layoutChanged.emit()

    '''
    def load_data(self, data):
        if type(data) == type(dict()):
            self.item=data
            tmp=[[i,data.get(i)] for i in data.keys() if i != 'address']
            #tmp.append(['address',str(data.get('address'))])
            data=tmp
        elif type(data) == type(list()):
            pass
            #convert list to dict
        self.fields = [i[0] for i in data]
        self.vals = [i[1] for i in data]

        self.column_count = 2
        self.row_count = len(self.vals)
    '''

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

    def flags(self,index):
        baseflags=QAbstractTableModel.flags(self,index)
        if index.column() == 1:
            if self.fields[index.row()] == "id":
                if self.ID_MODE == editable_table_enum.NON_EDITABLE_ID:
                    return baseflags

            return baseflags | Qt.ItemIsEditable
        else:
            return baseflags

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

    def listsToDict(self,fields_list:list,values_list:list) -> dict:
        return dict(zip(fields_list,values_list))

    def dataToItem(self) -> dict:
        return self.item

    def setData(self, index, value, role):
        #print(self.vals[index.row()],value) 
        if self.fields[index.row()] == 'state':
            self.vals[index.row()]=value[:2]
        else:
            self.vals[index.row()]=value

        self.dataChanged.emit(index,index)
        self.item=self.listsToDict(self.fields,self.vals)
        return True
