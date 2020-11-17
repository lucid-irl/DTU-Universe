from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ConvertThisQObject:

    """Class này hỗ trợ trình parse code của VSCode khi dùng uic kết nối file .ui với code backend Python."""

    def __init__(self, parent:QObject, qWidgetClass, connectString) -> None:
        self.parent = parent
        self.qobject = self.parent.findChild(qWidgetClass, connectString)

    def toQPushButton(self) -> QPushButton:
        return self.qobject

    def toQListWidget(self) -> QListWidget:
        return self.qobject

    def toQLineEdit(self) -> QLineEdit:
        return self.qobject

    def toQCheckBox(self) -> QCheckBox:
        return self.qobject

    def toQTextEdit(self) -> QTextEdit:
        return self.qobject

    def toQTableWidget(self) -> QTableWidget:
        return self.qobject

    def toQLabel(self) -> QLabel:
        return self.qobject
        
    def toQWidget(self) -> QWidget:
        return self.qobject
        
    def toQScrollArea(self) -> QScrollArea:
        return self.qobject