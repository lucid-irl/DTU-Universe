from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic

from class_convertType import ConvertThisQObject

import sys

class CustomDialogWindow(QWidget):

    def __init__(self) -> None:
        super(CustomDialogWindow, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        uic.loadUi('GUI\\custom_window.ui',self)
        self.frame_titleBar = ConvertThisQObject(self, QFrame, 'frame_titlebar').toQFrame()
        self.button = ConvertThisQObject(self, QPushButton, 'button_Cancel').toQPushButton()
        self.button.clicked.connect(lambda: self.close())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomDialogWindow()
    window.show()
    sys.exit(app.exec())