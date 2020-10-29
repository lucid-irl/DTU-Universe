# How to create a image button

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(200, 200)


app = QApplication(sys.argv)
window = QWidget()
layout = QHBoxLayout(window)

button = PicButton(QPixmap("Images\iconfinder_clipboard_download_50092.png"), QPixmap("Images\iconfinder_refresh_134221.png"), 
QPixmap("Images\iconfinder_checked-checklist-notepad_532781.png"))
layout.addWidget(button)

window.show()
sys.exit(app.exec_())