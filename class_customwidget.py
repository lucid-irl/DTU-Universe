from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget,QLabel, QHBoxLayout, QLayout, QPushButton

from class_custombutton import PicButton
from class_subject import Subject
# from main import Main

class QCustomQWidget(QWidget):
    """Custom layout cho item trong QListWidget."""

    def __init__ (self, subject: Subject, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.master = parent
        self.subject = subject
        status = self.subject.getStatus()

        self.textQVBoxLayout = QHBoxLayout()
        self.text_subjectname = QLabel(subject.name, self.master)
        self.label_status = QLabel(self.master)
        if status == 0:
            self.pixmap_status = QPixmap(r'Images\red_dot.png')
            self.label_status.setPixmap(self.pixmap_status)
            self.label_status.setToolTip('Không thể đăng ký')
        else:
            self.pixmap_status = QPixmap(r'Images\green_dot.png')
            self.label_status.setPixmap(self.pixmap_status)
            self.label_status.setToolTip('Có thể đăng ký')

        self.textQVBoxLayout.addWidget(self.label_status, 0, Qt.AlignLeft)
        self.textQVBoxLayout.addWidget(self.text_subjectname, 1, Qt.AlignLeft)


        self.textQVBoxLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.setLayout(self.textQVBoxLayout)

    def addButtonCopyIDSubject(self):
        self.button_copyIDToClipBoard = QPushButton('Sao chép ID', self)
        self.button_copyIDToClipBoard.clicked.connect(self.copyID)
        self.textQVBoxLayout.addWidget(self.button_copyIDToClipBoard,1)

    def copyID(self):
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(self.subject.getID())

    def addButtonAddToSemeter(self):
        self.button_add = PicButton(QPixmap('Images\icon_add.png'),QPixmap('Images\icon_add.png'),QPixmap('Images\icon_add.png'),self)
        self.textQVBoxLayout.addWidget(self.button_add, 0, Qt.AlignRight)
        self.button_add.clicked.connect(self.addThisSubjectToSemeter)
        self.button_add.setToolTip('Thêm môn này vào bảng')

    def addThisSubjectToSemeter(self):
        self.master.addSubjectToTable(self.subject)
