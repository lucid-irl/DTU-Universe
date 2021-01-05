from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ConvertThisQObject:

    """Class này hỗ trợ trình parse code của VSCode khi dùng uic kết nối file .ui với code backend Python."""

    def __init__(self, parent:QObject, qWidgetClass, connectString) -> None:
        self.parent = parent
        self.object = self.parent.findChild(qWidgetClass, connectString)

    def toQPushButton(self) -> QPushButton:
        return self.object

    def toQListWidget(self) -> QListWidget:
        return self.object

    def toQLineEdit(self) -> QLineEdit:
        return self.object

    def toQCheckBox(self) -> QCheckBox:
        return self.object

    def toQTextEdit(self) -> QTextEdit:
        return self.object

    def toQTableWidget(self) -> QTableWidget:
        return self.object

    def toQLabel(self) -> QLabel:
        return self.object
        
    def toQWidget(self) -> QWidget:
        return self.object
        
    def toQScrollArea(self) -> QScrollArea:
        return self.object

    def toQFrame(self) -> QFrame:
        return self.object

    def toQComboBox(self) -> QComboBox:
        return self.object

    def toQProgressBar(self) -> QProgressBar:
        return self.object

    def toQStackedWidget(self) -> QStackedWidget:
        return self.object


def toQCheckBox(object) -> QCheckBox:
    return object



