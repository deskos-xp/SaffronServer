from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QBuffer
from io import BytesIO

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

def pixmapToBytesIO(pixmap:QPixmap) -> BytesIO:
    #get image data
    bio=BytesIO()
    buff=QBuffer()
    buff.open(QBuffer.ReadWrite)
    pixmap.toImage().save(buff,"PNG")
    bio.write(buff.data())
    bio.seek(0)
    return bio


