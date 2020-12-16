from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget,QLabel, QHBoxLayout, QLayout, QPushButton

from class_subject import Subject

from win10toast import ToastNotifier
# from main import Main
## CustomListItemWidget
class CustomListItemWidget(QWidget):
    """Custom layout cho item trong QListWidget."""

    ICON_BUTTON_DELETE = 'Images\\3597038-text-editor\\svg\\007-delete.svg'
    ICON_BUTTON_COPY_ID = 'Images\\2921119-work-office-files\\svg\\010-info.svg'
    ICON_BUTTON_ADD = 'Images\\2921119-work-office-files\\svg\\019-add.svg'
    ICON_BUTTON_DETAILINFO = 'Images\\2921119-work-office-files\\svg\\010-info.svg'

    ICON_IMAGE_VALID = 'Images\\green_dot.png'
    ICON_IMAGE_INVALID = 'Images\\red_dot.png'

    signal_buttonAddIsPressed = pyqtSignal('PyQt_PyObject')
    signal_buttonDeleteIsPressed = pyqtSignal('PyQt_PyObject')
    signal_buttonShowDetailInfo = pyqtSignal('PyQt_PyObject')

    def __init__ (self, subject: Subject, parent=None):
        super(CustomListItemWidget, self).__init__(parent)
        self.master = parent
        self.subject = subject
        status = self.subject.getStatus()

        self.textQVBoxLayout = QHBoxLayout()
        self.text_subjectname = QLabel(subject.name, self.master)
        self.label_status = QLabel(self.master)
        if status == 0:
            self.pixmap_status = QPixmap(CustomListItemWidget.ICON_IMAGE_INVALID)
            self.label_status.setPixmap(self.pixmap_status)
            self.label_status.setToolTip('Không thể đăng ký')
        else:
            self.pixmap_status = QPixmap(CustomListItemWidget.ICON_IMAGE_VALID)
            self.label_status.setPixmap(self.pixmap_status)
            self.label_status.setToolTip('Có thể đăng ký')

        self.textQVBoxLayout.addWidget(self.label_status, 0, Qt.AlignLeft)
        self.textQVBoxLayout.addWidget(self.text_subjectname, 1, Qt.AlignLeft)


        self.textQVBoxLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.setLayout(self.textQVBoxLayout)

    def addButtonCopyIDSubject(self):
        self.button_copyIDToClipBoard = QPushButton()
        self.button_copyIDToClipBoard.setIcon(QIcon(CustomListItemWidget.ICON_BUTTON_COPY_ID))
        self.button_copyIDToClipBoard.clicked.connect(self.copyID)
        self.button_copyIDToClipBoard.setToolTip('Copy mã môn của môn này')
        self.textQVBoxLayout.addWidget(self.button_copyIDToClipBoard,0, Qt.AlignRight)

    def copyID(self):
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(self.subject.getID())
        toastCopied = ToastNotifier()
        toastCopied.show_toast("CS4RSA - Thông báo", "Bạn đã copy mã {0} vào Clipboard".format(self.subject.getID()), duration = 5, icon_path = "Images\logo.ico", threaded=True)

    def addButtonAddToSemeter(self):
        self.button_add = QPushButton()
        self.button_add.setIcon(QIcon(CustomListItemWidget.ICON_BUTTON_ADD))
        self.button_add.clicked.connect(self.addThisSubjectToSemeter)
        self.button_add.setToolTip('Thêm môn này vào bảng')
        self.textQVBoxLayout.addWidget(self.button_add, 0, Qt.AlignRight)

    def addThisSubjectToSemeter(self):
        self.signal_buttonAddIsPressed.emit(self.subject)

    def addButtonDelete(self):
        self.button_delete = QPushButton()
        self.button_delete.setIcon(QIcon(CustomListItemWidget.ICON_BUTTON_DELETE))
        self.button_delete.setToolTip('Xoá môn này')
        self.button_delete.clicked.connect(self.deleteThisSubjectToSemeter)
        self.textQVBoxLayout.addWidget(self.button_delete, 0, Qt.AlignRight)

    def deleteThisSubjectToSemeter(self):
        self.signal_buttonDeleteIsPressed.emit(self.subject)

    def addButtonShowDetailInfo(self):
        self.button_showDetailInfo = QPushButton()
        self.button_showDetailInfo.setIcon(QIcon())
        self.button_showDetailInfo.setToolTip('Thông tin chi tiết')
        self.button_showDetailInfo.clicked.connect(self.showDetailInfo)
        self.textQVBoxLayout.addWidget(self.button_showDetailInfo, 0, Qt.AlignRight)

    def showDetailInfo(self):
        self.signal_buttonShowDetailInfo.emit(self.subject)