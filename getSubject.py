from Crawl import Get_Url
from PyQt5.QtCore import QThread, pyqtSignal
from DataToExcel import CreateExcel

class ThreadGetSubject(QThread):
    foundExcel = pyqtSignal('PyQt_PyObject')
    nonFoundExcel = pyqtSignal('PyQt_PyObject')

    def __init__(self, name):
        QThread.__init__(self)
        try:
            self.name = name.split(' ')[0]
            self.id = name.split(' ')[1]
        except:
            self.nonFoundExcel.emit(False)

    
    def exist(self):
        if Get_Url(self.name, self.id) == None:
            self.nonFoundExcel.emit(False)

    def run(self):
        try:
            url = CreateExcel(self.name, self.id)
        except:
            self.nonFoundExcel.emit(False)
            return
        if url:
            self.foundExcel.emit(self.name+self.id+'.xls')
        else:
            self.nonFoundExcel.emit(False)
