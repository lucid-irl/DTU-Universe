"""Class này triển khai một giao diện cửa sổ trống. Bao gồm title, các nút phóng to, thu nhỏ và thoát cửa sổ.

window_title: QLable.
minimum_button: QPushButton.
maximum_button: QPushButton.
close_button: QPushButton."""

from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QDesktopWidget, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt
from PyQt5 import uic

from class_convertType import ConvertThisQObject

class Window(QWidget):
    WINDOW_IS_MAXIMIZED = False

    def __init__(self, connectString, minimumButton, maximumButton, closeButton, windowTitle):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.connectUi(connectString, minimumButton, maximumButton, closeButton, windowTitle)

    def connectUi(self, connectString, minimumButton, maximumButton, closeButton, windowTitle):
        uic.loadUi(connectString, self)
        self.minimumButton = ConvertThisQObject(self, QPushButton, minimumButton).toQPushButton()
        self.maximumButton = ConvertThisQObject(self, QPushButton, maximumButton).toQPushButton()
        self.closeButtun = ConvertThisQObject(self, QPushButton, closeButton).toQPushButton()
        self.minimumButton.clicked.connect(self.minimum)
        self.maximumButton.clicked.connect(self.maximum)
        self.closeButtun.clicked.connect(self.closeWindow)
        self.windowTitleLabel = ConvertThisQObject(self, QLabel, windowTitle).toQLabel()

    def closeWindow(self):
        self.close()

    def minimum(self):
        self.showMinimized()

    def maximum(self):
        if self.WINDOW_IS_MAXIMIZED:
            width = self.sizeHint().width()
            height = (QDesktopWidget().size().height()/100)*80
            centerPoint = QDesktopWidget().availableGeometry().center()
            self.hopePointX = centerPoint.x() - width/2
            self.hopePointY = centerPoint.y() - height/2
            self.qrect = QRect(self.hopePointX, self.hopePointY, width, height)
            self.ani = QPropertyAnimation(self, b'geometry')
            self.ani.setDuration(300)
            self.ani.setEndValue(self.qrect)
            self.ani.setEasingCurve(QEasingCurve.InOutQuad)
            self.ani.start()
            self.WINDOW_IS_MAXIMIZED = False
        else:
            self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            self.screenRect.setHeight(self.screenRect.height()-50)
            self.ani = QPropertyAnimation(self, b'geometry')
            self.ani.setDuration(300)
            self.ani.setEndValue(self.screenRect)
            self.ani.setEasingCurve(QEasingCurve.InOutQuad)
            self.ani.start()
            self.WINDOW_IS_MAXIMIZED = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos()-self.offset)

