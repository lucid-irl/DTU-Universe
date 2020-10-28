from os.path import basename
from Crawl import Get_Url
from PyQt5.QtCore import QThread, pyqtSignal
from DataToExcel import CreateExcel

class ThreadGetSubject(QThread):
    foundExcel = pyqtSignal('PyQt_PyObject')
    nonFoundExcel = pyqtSignal('PyQt_PyObject')

    def __init__(self, name):
        QThread.__init__(self)
        self.name = name
        try:
            self.sub = name.split(' ')[0]
            self.id = name.split(' ')[1]
        except:
            self.nonFoundExcel.emit(False)

    
    def exist(self):
        if Get_Url(self.sub, self.id) == None:
            self.nonFoundExcel.emit(False)

    def run(self):
        try:
            url = CreateExcel(self.sub, self.id)
        except:
            self.nonFoundExcel.emit(False)
            return
        if url:
            self.foundExcel.emit("Data/"+self.name+'.xls')
        else:
            self.nonFoundExcel.emit(False)
