from PyQt5.QtWidgets import QHeaderView
def setupViews(self,viewsList=[],modelsList=[]):
    def setupView(view,model):
        view.setModel(model)
        view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    #views=['userView','addressView','departmentView','roleView']
    #models=['userModel','addressModel','departmentModel','roleModel']

    for v,m in zip(viewsList,modelsList):
        view=getattr(self.dialog,v)
        model=getattr(self,m)
        setupView(view,model)


