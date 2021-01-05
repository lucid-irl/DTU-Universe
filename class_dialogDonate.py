from PyQt5.QtGui import QPicture, QPixmap
from class_convertType import ConvertThisQObject
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import uic
import team_config


class DonateWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        uic.loadUi(team_config.UI_DONATE, self)
        self.label_image = ConvertThisQObject(self, QLabel, 'label_image').toQLabel()
        self.button_ok = ConvertThisQObject(self, QPushButton, 'button_ok').toQPushButton()
        self.button_ok.clicked.connect(lambda: self.accept())

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.moving:
            self.move(event.globalPos()-self.offset)
