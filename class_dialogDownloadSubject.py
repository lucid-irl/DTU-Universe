import sys

from PyQt5.QtGui import QFont, QFontDatabase
from class_subject import Subject
from class_DTUCrawler import *
from class_DTUWeb import *
from class_subjectCrawler import SubjectPage, SubjectData
from class_convertType import ConvertThisQObject
import team_config

from PyQt5.QtWidgets import *
from PyQt5 import uic


class DownloadSubject(QWidget):

    def __init__(self):
        super(DownloadSubject, self).__init__()
        uic.loadUi(team_config.UI_DOWNLOAD_SUJECT, self)
        self.label_title = ConvertThisQObject(self, QLabel, 'labelTitle').toQLabel()
        self.label_title.setFont(QFont('Helvetica'))
        self.lalel_status = ConvertThisQObject(self, QLabel, 'labelStatus').toQLabel()
        self.button_cancel = ConvertThisQObject(self, QPushButton, 'pushButtonCancel').toQPushButton()
        self.progressbar = ConvertThisQObject(self, QProgressBar, 'progressBar').toQProgressBar()


class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        d = DownloadSubject()
        self.setCentralWidget(d)

QFontDatabase.addApplicationFont('fonts/TTF/helveticaneuebold.ttf')
print(QtCore.QDir('fonts/TTF'))
app = QApplication(sys.argv)
w = Main()
w.show()
app.exec_()