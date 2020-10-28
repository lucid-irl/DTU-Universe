
from PyQt5.QtWidgets import QWidget,QLabel, QHBoxLayout, QLayout
from class_subject import Subject


class QCustomQWidget (QWidget):
    """Custom layout cho item trong QListWidget."""
    def __init__ (self,  subject: Subject, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.master = parent
        self.subject = subject
        status = self.subject.getStatus()

        self.textQVBoxLayout = QHBoxLayout()
        self.text_subjectname = QLabel(subject.name, self.master)
        self.textQVBoxLayout.addWidget(self.text_subjectname)
        self.textQVBoxLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.textQVBoxLayout)

        
        

