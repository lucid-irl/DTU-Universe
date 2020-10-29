from os.path import basename
from Crawl import Get_Url
from PyQt5.QtCore import QThread, pyqtSignal
from DataToExcel import CreateExcel

class ThreadGetSubject(QThread):
    signal_foundExcel = pyqtSignal('PyQt_PyObject')
    signal_nonFoundExcel = pyqtSignal('PyQt_PyObject')

    def __init__(self, name):
        QThread.__init__(self)
        self.name = name
        try:
            self.sub = name.split(' ')[0]
            self.id = name.split(' ')[1]
        except:
            self.signal_nonFoundExcel.emit(False)

    
    def exist(self):
        if Get_Url(self.sub, self.id) == None:
            self.signal_nonFoundExcel.emit(False)

    def run(self):
        try:
            url = CreateExcel(self.sub, self.id)
        except:
            self.signal_nonFoundExcel.emit(False)
            return
        if url:
            self.signal_foundExcel.emit("Data/"+self.name+'.xls')
        else:
            self.signal_nonFoundExcel.emit(False)
