import sys
from PyQt5.QtWidgets import QWidget,QLabel, QHBoxLayout
from subject import Subject

class QCustomQWidget (QWidget):
    '''Khởi tạo widgit'''
    def __init__ (self,  subject: Subject, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.master = parent
        self.subject = subject
        self.textQVBoxLayout = QHBoxLayout()
        self.text_subjectname = QLabel(subject.name, self.master)
        self.textQVBoxLayout.addWidget(self.text_subjectname)
        self.setLayout(self.textQVBoxLayout)

        
        

