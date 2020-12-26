from class_subject import Subject
from PyQt5.QtWidgets import QWidget, QHBoxLayout,  QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CustomConflictWidget(QWidget):

    def __init__(self, subject1: Subject, subject2: Subject, parent=None) -> None:
        super(CustomConflictWidget, self).__init__(parent=parent)
        self.subject1 = subject1
        self.subject2 = subject2
        self.setupUI()

    def setupUI(self):
        self.hboxlayout = QHBoxLayout()
        self.label_subjectName1 = QLabel(self.subject1.getSubjectCode(), self)
        self.label_subjectName1.setAlignment(Qt.AlignCenter)
        self.label_subjectName2 = QLabel(self.subject2.getSubjectCode(), self)
        self.label_subjectName2.setAlignment(Qt.AlignCenter)
        self.pixmap_icon = QPixmap(r'Images\red_dot.png')
        self.label_image = QLabel(self)
        self.label_image.setPixmap(self.pixmap_icon)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.hboxlayout.addWidget(self.label_subjectName1, 2)
        self.hboxlayout.addWidget(self.label_image, 1)
        self.hboxlayout.addWidget(self.label_subjectName2, 2)
        self.setLayout(self.hboxlayout)