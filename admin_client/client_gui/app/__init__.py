from PyQt5.QtWidgets import QGridLayout
import inspect,os
def getLocalizedPath():
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        return filename,path

