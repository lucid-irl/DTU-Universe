from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from class_semester import *

import sys

class WeeksChoicer(QDialog):
    
    choiceWeek = pyqtSignal('PyQt_PyObject')

    def __init__(self, maxWeek) -> None:
        super().__init__()
        self.setWindowTitle('Chọn tuần học')
        self.maxWeek = maxWeek
        self.setupUI()

    def setupUI(self):
        self.qgridbox = QGridLayout(self)
        maxItemInRow = 5
        count = 0
        row = 0
        while count<self.maxWeek:
            for column in range(0, maxItemInRow):
                self.weekButton = QPushButton(str(count+1), self)
                self.weekButton.value = count+1
                self.weekButton.clicked.connect(lambda b, value=self.weekButton.value: self.showWeek(value))
                self.qgridbox.addWidget(self.weekButton, row, column)
                count+=1
                if count == self.maxWeek:
                    break
            row+=1
        self.setLayout(self.qgridbox)

    def showWeek(self, value):
        self.choiceWeek.emit(value)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WeeksChoicer(13)
    w.show()
    sys.exit(app.exec())

