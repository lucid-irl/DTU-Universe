from PyQt5.QtCore import QThread, pyqtSignal
from crawlSubject import *
from schedule import Schedule

class ThreadGetSubject(QThread):
    foundExcel = pyqtSignal()
    nonFoundExcel = pyqtSignal()

    def __init__(self, parent, name: str, id: str):
        QThread.__init__(self, parent=parent)
        self.name = name
        self.id = id

    def run(self):
        url = GetURL(self.name, self.id)
        if url != None:
            self.foundExcel.emit()
        else:
            self.nonFoundExcel.emit()
