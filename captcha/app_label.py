from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from class_convertType import ConvertThisQObject
import os
import sys
import crawl_captcha
import cut_captcha
import re

class App(QWidget):

    FOLDER_SRC = 'resolved_captchas'

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        if os.path.exists(self.FOLDER_SRC) == False:
            os.mkdir(self.FOLDER_SRC)
        uic.loadUi('label_app.ui', self)
        self.button_next = ConvertThisQObject(self, QPushButton, 'button_next').toQPushButton()
        self.edit_text = ConvertThisQObject(self, QLineEdit, 'edit_text').toQLineEdit()
        self.label_captcha = ConvertThisQObject(self, QLabel, 'label_captcha').toQLabel()
        self.load_captcha()
        self.connectSignal()
        self.connectHotKey()
    
    def connectSignal(self):
        self.button_next.clicked.connect(self.next)

    def connectHotKey(self):
        self.button_next.setShortcut('Return')
    
    def load_captcha(self):
        self.edit_text.setFocus()
        captcha_id = crawl_captcha.get_captcha_id()
        crawl_captcha.download_captcha_image(captcha_id, self.FOLDER_SRC)
        self.file_name = self.FOLDER_SRC+'\\'+captcha_id+'.jpeg'
        self.image = QPixmap(self.file_name)
        self.label_captcha.setPixmap(self.image)

    def next(self):
        self.captcha_text = self.edit_text.text().upper()
        if re.search('[A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9]', self.captcha_text):
            new_name = self.FOLDER_SRC+'\\'+self.captcha_text+'.jpeg'
            os.rename(self.file_name, new_name)
            cut_captcha.cut_captcha_with_name_is_resolved(new_name)
        else:
            print('invalid text')
            os.remove(self.file_name)
        self.load_captcha()
        self.edit_text.clear()
    
    def close(self) -> bool:
        if re.search('[A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9]', self.captcha_text):
            new_name = self.FOLDER_SRC+'\\'+self.captcha_text+'.jpeg'
            os.rename(self.file_name, new_name)
            super().close()
        else:
            os.remove(self.file_name)
            super().close()
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())