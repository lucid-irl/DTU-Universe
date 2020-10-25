from PyQt5.QtCore import QThread, pyqtSignal
from DataToExcel import CreateExcel
from schedule import Schedule

class ThreadGetSubject(QThread):
    foundExcel = pyqtSignal('PyQt_PyObject')
    nonFoundExcel = pyqtSignal('PyQt_PyObject')

    def __init__(self, name: str, id: str):
        QThread.__init__(self)
        self.name = name
        self.id = id

    def run(self):
        url = CreateExcel(self.name, self.id)
        if url:
            self.foundExcel.emit(self.name+self.id+'.xls')
        else:
            self.nonFoundExcel.emit(False)
