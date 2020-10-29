
from PyQt5.QtWidgets import QWidget,QLabel, QHBoxLayout, QLayout
from class_subject import Subject
from PyQt5.QtGui import QPixmap

class QCustomQWidget (QWidget):
    """Custom layout cho item trong QListWidget."""
    def __init__ (self,  subject: Subject, parent = None):
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
        else:
            self.pixmap_status = QPixmap(r'Images\green_dot.png')
            self.label_status.setPixmap(self.pixmap_status)

        self.textQVBoxLayout.addWidget(self.label_status, 0)
        self.textQVBoxLayout.addWidget(self.text_subjectname, 1)

        self.textQVBoxLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.textQVBoxLayout)

    
    

