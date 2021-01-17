from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from class_subject import Subject
from PyQt5 import uic
import team_config
from class_convertType import ConvertThisQObject


class DetailClassInfoWindow(QDialog):
    def __init__(self, subject: Subject):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.subject = subject
        uic.loadUi(team_config.UI_DETAILCLASSINFO, self)
        self.button_ok = ConvertThisQObject(self, QPushButton, 'button_ok').toQPushButton()
        self.button_ok.clicked.connect(lambda: self.accept())
        self.label_content = ConvertThisQObject(self, QLabel, 'label_content').toQLabel()
        self.label_subtitle = ConvertThisQObject(self, QLabel, 'label_subtitle').toQLabel()
        self.label_title = ConvertThisQObject(self, QLabel, 'label_title').toQLabel()
        self.setupUI()

    def setupUI(self):
        self.label_title.setText(self.subject.getSubjectCode())
        self.label_subtitle.setText(self.subject.getName())
        places = ', '.join(self.subject.getLocations())
        stringFullDateTime = []
        for date in self.subject.getSchedule().getDatesOfLesson():
            times = self.subject.getSchedule().getTimeOfDate(date)
            timeString = ', '.join(times)
            dateTime = '{0} ({1})'.format(date, timeString)
            stringFullDateTime.append(dateTime)
        joinedStringFullDateTime = ', '.join(stringFullDateTime)
        rooms = ', '.join(self.subject.getRooms())
        if self.subject.getTeachers() != [""]:
            teachers = ', '.join(self.subject.getTeachers())
        else:
            teachers = 'Không rõ'
        self.content = """
            <html>

            <head />

            <body>
            Mã đăng ký: {0}
            <br>
            Số tín chỉ: {13} ({14})
            <br>
            Loại hình: {1}
            <br>
            Còn trống: <b>{2}</b>
            <br>
            Ngày bắt đầu đăng ký: {3}
            <br>
            Ngày kết thúc đăng ký: {4}
            <br>
            Tuần bắt đầu: <b>{5}</b>
            <br>
            Tuần kết thúc: <b>{6}</b>
            <br>
            Nơi học: <b>{7}</b>
            <br>
            Học vào các thứ: <b>{8}</b>
            <br>
            Học tại các phòng: {9}
            <br>
            Giảng viên đứng lớp: <b>{10}</b>
            <br>
            Trạng thái đăng ký: {11}
            <br>
            Tình trạng triển khai: {12}
            </body>

            </html>
        """.format(
            self.subject.getRegisterCode(),
            self.subject.getType(),
            self.subject.getEmptySeat(),
            self.subject.getRegistrationTermStart(),
            self.subject.getRegistrationTermEnd(),
            self.subject.getWeekStart(),
            self.subject.getWeekEnd(),
            places,
            joinedStringFullDateTime,
            rooms,
            teachers,
            self.subject.getRegistrationStatus(),
            self.subject.getImplementationStatus(),
            self.subject.getCredit(),
            ' '.join(self.subject.getCreditDetail())
        )
        self.label_content.setTextFormat(Qt.RichText)
        self.label_content.setText(self.content)

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.moving:
            self.move(event.globalPos()-self.offset)