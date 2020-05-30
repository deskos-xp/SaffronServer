from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QFileDialog

def pathToQPixmap(path) -> QPixmap:
    try:
        return QPixmap(path)
    except Exception as e:
        print(e)
        return None

def getFilePathDialog(caption,) -> str:
        fname = QFileDialog.getOpenFileName(None, caption,'.',"Image files (*.jpg *.gif *.png)") 
        if fname: 
            return fname[0]


