from typing import List
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic

from class_convertType import ConvertThisQObject

import sys


class CustomDialogButton(QPushButton):

    def __init__(self) -> None:
        super(CustomDialogButton, self).__init__()
        
    def addSignal(self, signal: pyqtSignal):
        self.signal = signal

    def getSignal(self):
        return self.signal


class CustomDialogWindow(QWidget):
    """
    Class này triển khai một Custom Window cho các Dialog Box block Main Window.
    Các Button bên trong được thêm thông qua phương thức addButton()
    """
    UI = 'GUI\\custom_window.ui'

    def __init__(self, title: str, content: str, image=None) -> None:
        super(CustomDialogWindow, self).__init__()
        self.title = title
        self.content = content
        self.buttons = []
        self.image = image
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        uic.loadUi(self.UI,self)
        self.frame_titleBar = ConvertThisQObject(self, QFrame, 'frame_titlebar').toQFrame()
        self.button = ConvertThisQObject(self, QPushButton, 'button_Cancel').toQPushButton()
        self.button.clicked.connect(lambda: self.close())

    def addButton(self, name: str, button: QPushButton, signal: pyqtSignal):
        """#### Thêm button vào custom window.
        
        """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomDialogWindow(None, None)
    window.show()
    sys.exit(app.exec())