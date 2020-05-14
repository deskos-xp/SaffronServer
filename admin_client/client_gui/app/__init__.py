from PyQt5.QtWidgets import QGridLayout


def clearGrid(self,complete=False):
    if complete == False:

        for i in range(self.w.product_view.count()):
            try:
                q=self.w.product_view.takeAt(i).widget()
                self.w.product_view.removeWidget(q)
                q.deleteLater()
                del(q)
            except:
                q=self.w.product_view.takeAt(i)
                self.w.product_view.removeItem(q)
                del(q)
    else:
        pass
    self.w.product_view.update()

