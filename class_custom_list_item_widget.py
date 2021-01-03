from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget,QLabel, QHBoxLayout, QLayout, QPushButton

from class_subject import Subject
from class_dialogDetailInfo import DetailClassInfoWindow

from win10toast import ToastNotifier
# from main import Main
## CustomListItemWidget
class CustomListItemWidget(QWidget):
    """Custom layout cho item trong QListWidget."""

    ICON_BUTTON_DELETE = 'resources/007-delete.svg'
    ICON_BUTTON_COPY_ID = 'resources/icons8-paste-96.png'
    ICON_BUTTON_ADD = 'resources/icon_add.svg'
    ICON_BUTTON_DETAILINFO = 'resources/icons8-info.svg'

    ICON_IMAGE_VALID = 'Images\\green_dot.png'
    ICON_IMAGE_INVALID = 'Images\\red_dot.png'

    signal_buttonAddIsPressed = pyqtSignal('PyQt_PyObject')
    signal_buttonDeleteIsPressed = pyqtSignal('PyQt_PyObject')
    signal_buttonShowDetailInfo = pyqtSignal('PyQt_PyObject')

    def __init__ (self, subject: Subject, parent=None):
        super(CustomListItemWidget, self).__init__(parent)
        self.master = parent
        self.subject = subject
        status = self.subject.getRegistrationStatus()

        self.textQVBoxLayout = QHBoxLayout()
        self.text_subjectname = QLabel(subject.getSubjectCode(), self.master)
        self.label_status = QLabel(self.master)
        if not status == 'Còn Hạn Đăng Ký':
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

        stringFullDateTime = []
        for date in self.subject.getSchedule().getDatesOfLesson():
            times = self.subject.getSchedule().getTimeOfDate(date)
            timeString = ', '.join(times)
            dateTime = '{0} ({1})'.format(date, timeString)
            stringFullDateTime.append(dateTime)
        joinedStringFullDateTime = ', '.join(stringFullDateTime)
        if self.subject.getTeachers() != [""]:
            teachers = ', '.join(self.subject.getTeachers())
        else:
            teachers = 'Không rõ'
        places = ', '.join(self.subject.getLocations())
        toolTip = '<b>{0}</b><br>{1}<br>{2}'.format(teachers, places, joinedStringFullDateTime)

        self.setToolTip(toolTip)

        #right click to delete subject

    def addRightClickToRemove(self, event):
        if event.button() == Qt.RightButton:
            self.deleteThisSubjectToSemeter()

    def removeWhenRightClick(self):
        self.mousePressEvent = lambda e: self.addRightClickToRemove(e)

    def addButtonCopyIDSubject(self):
        self.button_copyIDToClipBoard = QPushButton()
        self.button_copyIDToClipBoard.setIcon(QIcon(CustomListItemWidget.ICON_BUTTON_COPY_ID))
        self.button_copyIDToClipBoard.clicked.connect(self.copyID)
        self.button_copyIDToClipBoard.setToolTip('Copy mã môn của môn này')
        self.textQVBoxLayout.addWidget(self.button_copyIDToClipBoard,0, Qt.AlignRight)

    def copyID(self):
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(self.subject.getRegisterCode())
        toastCopied = ToastNotifier()
        title = "CS4RSA - Thông báo"
        textNoti = "Bạn đã copy mã {0} vào Clipboard".format(self.subject.getRegisterCode())
        toastCopied.show_toast(title, textNoti, duration = 5, icon_path = "Images\logo.ico", threaded=True)

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
        self.button_showDetailInfo.setIcon(QIcon(CustomListItemWidget.ICON_BUTTON_DETAILINFO))
        self.button_showDetailInfo.setToolTip('Thông tin chi tiết')
        self.button_showDetailInfo.clicked.connect(self.showDetailInfo)
        self.textQVBoxLayout.addWidget(self.button_showDetailInfo, 0, Qt.AlignRight)

    def showDetailInfo(self):
        self.detailInfo = DetailClassInfoWindow(self.subject).exec()