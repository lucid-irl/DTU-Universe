from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import team_config
import sys


class CalendarChoicer(QWidget):

    signal_OK_Pressed = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        print(team_config.CALENDAR_CHOICE_UI_PATH)
        uic.loadUi(team_config.CALENDAR_CHOICE_UI_PATH, self)
        self.button_OK = self.findChild(QPushButton, 'pushButton_OK')
        self.calendar = self.findChild(QCalendarWidget, 'calendarWidget')

        # temp
        self.button_OK = QPushButton()
        self.calendar = QCalendarWidget()

    def connectSignals(self):
        self.button_OK.clicked.connect(self.button_OK_clicked)

    def button_OK_clicked(self):
        qdate = self.calendar.selectedDate()
        self.signal_OK_Pressed.emit(qdate)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarChoicer()
    window.show()
    sys.exit(app.exec_())
