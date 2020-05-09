from PyQt5.QtWidgets import QComboBox

class ComboBox_Update:
    debug=False
    def __init__(self):
        pass

    def needs_update(self,cb:QComboBox,new_data:list):
        if self.debug == True:
            print(new_data)
        if cb.count() <= 0:
            cb.addItems(new_data)
        else:
            self.update(cb,new_data)

    def update(self,cb:QComboBox,new_data:list):
        for units_name in new_data:
            res=cb.findText(units_name)
            if res < 0:
                cb.addItem(units_name)


