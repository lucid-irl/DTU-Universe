from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import team_config
import sys


class CalendarChoicer(QWidget):

    def __init__(self) -> None:
        super().__init__()
        print(team_config.CALENDAR_CHOICE_UI_PATH)
        uic.loadUi(team_config.CALENDAR_CHOICE_UI_PATH, self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarChoicer()
    window.show()
    sys.exit(app.exec_())
