from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import team_config
import sys


class CalendarChoicer(QDialog):

    signal_OK_Pressed = pyqtSignal('PyQt_PyObject')
    def __init__(self,*args, **kwargs) -> None:
        super(CalendarChoicer, self).__init__(*args, **kwargs)
        print(team_config.CALENDAR_CHOICE_UI_PATH)
        uic.loadUi(team_config.CALENDAR_CHOICE_UI_PATH, self)
        self.buttonBox = self.findChild(QDialogButtonBox, 'buttonBox')
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarChoicer()
    window.show()
    sys.exit(app.exec_())
