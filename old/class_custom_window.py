from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

from class_convertType import ConvertThisQObject

import os


class CustomDialogWindow(QDialog):

    UI = 'GUI\\custom_window.ui'
    signal_OK_is_pressed = pyqtSignal('PyQt_PyObject')

    def __init__(self, title: str=None, content: str=None, imagePath=None) -> None:
        super(CustomDialogWindow, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.title = title
        self.content = content
        self.imagePath = imagePath

        uic.loadUi(self.UI,self)
        self.frame_titleBar = ConvertThisQObject(self, QFrame, 'frame_titlebar').toQFrame()
        self.button_cancel = ConvertThisQObject(self, QPushButton, 'button_cancel').toQPushButton()
        self.button_OK = ConvertThisQObject(self, QPushButton, 'button_OK').toQPushButton()
        self.label_title = ConvertThisQObject(self, QLabel, 'label_title').toQLabel()
        self.label_content = ConvertThisQObject(self, QLabel, 'label_content').toQLabel()
        self.label_image = ConvertThisQObject(self, QLabel, 'label_image').toQLabel()
        self.fillDataToDialog()

        self.connectSignal()


    def fillDataToDialog(self):
        if self.title:
            self.label_title.setText(self.title)
        if self.content:
            self.label_content.setText(self.content)
        if self.imagePath and os.path.exists(self.imagePath):
            if os.path.splitext(self.imagePath)[1] == '.gif':
                gif = QMovie(self.imagePath)
                self.label_image.setMovie(gif)
                gif.start()
                return
            image = QPixmap(self.imagePath)
            self.label_image.setPixmap(image)

    def connectSignal(self):
        self.button_cancel.clicked.connect(self.closeWindow)
        self.button_OK.clicked.connect(self.closeWindowAndEmitSignal)

    def closeWindowAndEmitSignal(self):
        self.close()
        self.signal_OK_is_pressed.emit(True)

    def closeWindow(self):
        self.close()

    def minimum(self):
        self.showMinimized()

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.moving:
            self.move(event.globalPos()-self.offset)
