from PyQt5.QtWidgets import (QShortcut, QStackedWidget, QWidget, QApplication, QPushButton, QListWidget, QListWidgetItem,
                            QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QLabel, 
                            QFrame, QScrollArea, QCompleter, QDesktopWidget)
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QColor, QKeySequence, QValidator 
from PyQt5 import uic

from class_custom_list_item_widget import CustomListItemWidget
from class_customConflictWidget import CustomConflictWidget
from class_semester import Semester, WEEK
from class_subject import Subject
from class_convertType import ConvertThisQObject
from class_flow_layout import FlowLayout
from class_subjectCrawler import *
from class_dialogNotification import NotificationWindow
from class_homeCourseSearch import HomeCourseSearch
from class_setting import Setting
from thread_downloadSubject import ThreadDownloadSubject, ThreadShowLoading

from typing import List

import sys
import os
import cs4rsa_color
import team_config


class ValidatorFindLineEdit(QValidator):
    """In hoa mọi ký tự nhập vào QLineEdit."""
    def validate(self, string, pos):
        return QValidator.Acceptable, string.upper(), pos

class Main(QWidget):
    """Class này chỉ đảm nhiệm việc xử lý giao diện."""

    SUBJECT_FOUND:List[Subject] = []
    CURRENT_SUBJECT:str = ''
    WINDOW_IS_MAXIMIZED = False

    # Các phương thức setting Giao diện bao gồm kết nối Signal, add Hot key,...
    def __init__(self):
        super(Main, self).__init__() #Main, self
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.semester = Semester()
        self.setting = Setting('cs4rsa_settings.json')
        self.currentSchoolYearValue = HomeCourseSearch.getCurrentSchoolYearValue()
        uic.loadUi(team_config.FOLDER_UI+'/'+team_config.USE_UI, self)

        self.button_findSubject = ConvertThisQObject(self, QPushButton, 'pushButton_timKiem').toQPushButton()
        self.button_updateSubject = ConvertThisQObject(self, QPushButton, 'pushButton_capNhat').toQPushButton()
        self.button_register = ConvertThisQObject(self, QPushButton, 'pushButton_dangKy').toQPushButton()
        self.button_saveExcel = ConvertThisQObject(self, QPushButton, 'pushButton_luuText').toQPushButton()
        self.button_nextWeek = ConvertThisQObject(self, QPushButton, 'pushButton_nextWeek').toQPushButton()
        self.button_previousWeek = ConvertThisQObject(self, QPushButton, 'pushButton_previousWeek').toQPushButton()
        self.button_gotoWeek = ConvertThisQObject(self, QPushButton, 'pushButton_goto').toQPushButton()

        # title bar
        self.button_close = ConvertThisQObject(self, QPushButton, 'pushButton_close').toQPushButton()
        self.button_maximum = ConvertThisQObject(self, QPushButton, 'pushButton_maximum').toQPushButton()
        self.button_minimum = ConvertThisQObject(self, QPushButton, 'pushButton_minimum').toQPushButton()

        # navigation bar
        self.stackedWidget = ConvertThisQObject(self, QStackedWidget, 'stackedWidget').toQStackedWidget()
        self.stackedWidget.setCurrentIndex(0)

        self.frame_navi = ConvertThisQObject(self, QFrame, 'frame_navbar').toQFrame()
        self.button_menu = ConvertThisQObject(self, QPushButton, 'pushButton_menu').toQPushButton()
        self.button_nav_setting = ConvertThisQObject(self, QPushButton, 'button_nav_setting').toQPushButton()
        self.button_nav_predict = ConvertThisQObject(self, QPushButton, 'button_nav_predict').toQPushButton()
        self.button_nav_home = ConvertThisQObject(self, QPushButton, 'button_nav_home').toQPushButton()
        self.button_nav_info = ConvertThisQObject(self, QPushButton, 'button_nav_info').toQPushButton()

        self.listView_SubjectDownloaded = ConvertThisQObject(self, QListWidget, 'listWidget_tenLop').toQListWidget()
        self.listView_SubjectChoiced = ConvertThisQObject(self, QListWidget, 'listWidget_lopDaChon').toQListWidget()
        self.listView_SubjectConflict = ConvertThisQObject(self, QListWidget, 'listWidget_lopXungDot').toQListWidget()

        self.label_week = ConvertThisQObject(self, QLabel, 'label_week').toQLabel()
        self.label_windowTitle = ConvertThisQObject(self, QLabel, 'label_windowTitle').toQLabel()

        self.currentSchoolYearInfo = HomeCourseSearch.getCurrentSchoolYearInfo()
        self.currentSemesterInfo = HomeCourseSearch.getCurrentSemesterInfo()
        self.dynamicTitle = team_config.TITLE+' • <b>{0}</b> • {1}'.format(self.currentSchoolYearInfo, self.currentSemesterInfo)
        self.label_windowTitle.setText(self.dynamicTitle)

        self.line_findSubject = ConvertThisQObject(self, QLineEdit, 'lineEdit_tenMon').toQLineEdit()
        self.line_findSubject.mousePressEvent = lambda _ : self.line_findSubject.selectAll()
        self.line_findSubject.setValidator(ValidatorFindLineEdit())
        allSubject = HomeCourseSearch.getDisciplineFromFile('allDiscipline.json')
        completer = QCompleter(allSubject)
        self.line_findSubject.setCompleter(completer)

        self.table_Semeter = ConvertThisQObject(self, QTableWidget, 'tableWidget_lichHoc').toQTableWidget()

        self.scroll_buttonWeek = ConvertThisQObject(self, QScrollArea, 'scrollArea').toQScrollArea()
        self.widget_buttonWeekContainer = ConvertThisQObject(self, QWidget, 'weeks_container').toQWidget()
        self.flowlayout = FlowLayout()
        self.widget_buttonWeekContainer.setLayout(self.flowlayout)
        self.scroll_buttonWeek.setWidget(self.widget_buttonWeekContainer)
        self.scroll_buttonWeek.setWidgetResizable(True)

        width = (QDesktopWidget().size().width()/100)*80
        height = (QDesktopWidget().size().height()/100)*80
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.hopePointX = centerPoint.x() - width/2
        self.hopePointY = centerPoint.y() - height/2
        self.qrect = QRect(self.hopePointX, self.hopePointY, width, height)
        self.setGeometry(self.qrect)
        self.WINDOW_IS_MAXIMIZED = False

        self.connectSignals()
        self.addShortcut()

    def connectSignals(self):
        """Phương thức này kết nối signal với slot tương ứng."""
        self.button_findSubject.clicked.connect(self.actionFindSubject)
        self.button_register.clicked.connect(self.register)
        self.button_updateSubject.clicked.connect(self.updateSubject)
        self.button_previousWeek.clicked.connect(self.actionGoToPreviousWeek)
        self.button_nextWeek.clicked.connect(self.actionGoToNextWeek)

        self.button_close.clicked.connect(self.closeWindow)
        self.button_maximum.clicked.connect(self.maximum)
        self.button_minimum.clicked.connect(self.minimum)
        self.button_menu.clicked.connect(self.expandNavbar)

        self.button_nav_home.clicked.connect(lambda _: self.actionChangeFrame(0))
        self.button_nav_predict.clicked.connect(lambda _: self.actionChangeFrame(1))
        self.button_nav_setting.clicked.connect(lambda _: self.actionChangeFrame(2))
        self.button_nav_info.clicked.connect(lambda _: self.actionChangeFrame(3))
        
        # Các đối tượng dữ liệu
        self.semester.signal_indexChanged.connect(lambda: self.loadButtonWeekContainer(self.semester.getMaxWeekInSemester()))
        self.semester.singal_addSubject.connect(self.afterAddSubject)
        self.semester.signal_deleteSubject.connect(self.afterDeleteSubject)

    def addShortcut(self):
        """Phương thức này chịu trách nhiệm gán Shortcut cho các chức năng trong ứng dụng."""
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.close)

        # shortcut for button here
        self.button_findSubject.setShortcut('Ctrl+F')
        self.button_maximum.setShortcut('F')

    # IMPORTANT!!!
    # Các phương thức này chuẩn bị đủ đúng context trước khi thao tác, ta gọi chúng là Action

    def actionFindSubject(self):
        disciplineData = HomeCourseSearch.getDisciplineFromFile('allDiscipline.json')
        subjectName = toStringAndCleanSpace(self.line_findSubject.text())
        if subjectName:
            if not subjectName in disciplineData:
                NotificationWindow('Thông báo','Nhập sai mã môn rồi bạn gì đó ơi','Cảm ơn đã nhắc mình').exec_()
            else:
                discipline = subjectName.upper().split(' ')[0]
                keyword1 = subjectName.split(' ')[1]
                self.findSubject(discipline, keyword1)
        else:
            NotificationWindow('Thông báo','Chưa nhập mã môn kìa bạn','Cảm ơn đã nhắc mình').exec_()

    def actionGoToPreviousWeek(self):
        if self.semester.getCurrentSemesterIndex():
            self.gotoPreviousWeek()

    def actionGoToNextWeek(self):
        if self.semester.getCurrentSemesterIndex():
            self.gotoNextWeek()

    def actionChangeFrame(self, frameIndex):
        print('Change frame')
        self.stackedWidget.setCurrentIndex(frameIndex)
        

    # IMPORTANT!!!
    # Các phương thức load giao diện quan trọng
    def loadTable(self, subjects: List[Subject]):
        self.resetColorTable()
        if subjects == []:
            return
        for subject in subjects:
            days = subject.getSchedule().getDatesOfLesson()
            color = QColor(subject.getColor())
            for day in days:
                start_time_subjects = subject.getSchedule().getStartTimeOfDate(day)
                end_time_subjects = subject.getSchedule().getEndTimeOfDate(day)
                for i in range(len(start_time_subjects)):
                    start = str(start_time_subjects[i])
                    end = str(end_time_subjects[i])
                    start_row = self.semester.getTimeChains()[start]
                    end_row = self.semester.getTimeChains()[end]
                    column = WEEK.index(day)
                    for pen in range(start_row, end_row+1):
                        item = QTableWidgetItem()
                        item.setText(subject.getSubjectCode())
                        item.setBackground(color)
                        item.setToolTip(subject.getSubjectCode() +'•'+ subject.getName())
                        self.table_Semeter.setItem(pen, column, item)
        self.paintConflict()

    def loadListConflict(self):
        """Load List Widget chứa thông tin Subject Conflict."""
        self.listView_SubjectConflict.clear()
        for conflict in self.semester.getConflicts():
            sub1 = conflict.getSubject1()
            sub2 = conflict.getSubject2()

            self.custom_conflict_widget = CustomConflictWidget(sub1, sub2)

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectConflict)
            self.myQListWidgetItem.setData(Qt.UserRole, conflict)
            self.myQListWidgetItem.setSizeHint(self.custom_conflict_widget.sizeHint())

            self.listView_SubjectConflict.setItemWidget(self.myQListWidgetItem, self.custom_conflict_widget)
            self.listView_SubjectConflict.addItem(self.myQListWidgetItem)

    def loadListSubjectChoiced(self):
        """Phương thức này sẽ làm sạch danh sách môn đã chọn và tải lại nó từ list môn học hiện có trong Semester."""
        self.listView_SubjectChoiced.clear()
        for subject in self.semester.getSubjects():

            self.custom_widget_subject = CustomListItemWidget(subject)
            self.custom_widget_subject.addButtonCopyIDSubject()
            self.custom_widget_subject.addButtonDelete()
            self.custom_widget_subject.signal_buttonDeleteIsPressed.connect(self.deleteSubject)

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectChoiced)
            self.myQListWidgetItem.setData(Qt.UserRole, subject)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())

            self.listView_SubjectChoiced.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)
            self.listView_SubjectChoiced.addItem(self.myQListWidgetItem)

    def loadListSubjectFound(self):
        for subject in self.SUBJECT_FOUND:
            self.custom_widget_subject = CustomListItemWidget(subject, self)
            self.custom_widget_subject.addButtonAddToSemeter()
            self.custom_widget_subject.signal_buttonAddIsPressed.connect(self.addSubject)

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectDownloaded)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())
            self.myQListWidgetItem.setData(Qt.UserRole, subject)

            self.listView_SubjectDownloaded.addItem(self.myQListWidgetItem)
            self.listView_SubjectDownloaded.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)

    def loadButtonWeekContainer(self, maxWeek):
        """Render các button để điều hướng trong các Tuần của Semester."""
        for i in reversed(range(self.flowlayout.count())):
            self.flowlayout.itemAt(i).widget().deleteLater()
        if maxWeek == 0:
            self.flowlayout.clear()
        else:
            for index in range(maxWeek):
                self.weekButton = QPushButton(str(index+1), self)
                if index == self.semester.getCurrentSemesterIndex():
                    self.weekButton.setStyleSheet('background-color: #2980b9; color: white;')
                self.weekButton.setFixedWidth(40)
                self.weekButton.setFixedHeight(40)
                self.weekButton.clicked.connect(lambda b, value=index+1: self.gotoWeek(value))
                self.flowlayout.addWidget(self.weekButton)

    def loadLabelWeek(self):
        if self.semester.getSubjects():
            self.label_week.setText('Tuần '+str(self.semester.getCurrentSemesterIndex()+1))
        else:
            self.label_week.setText('Tuần ?')

    # IMPORTANT!!!
    # Các phương thức thao tác trên Subject
    def deleteSubject(self, subject: Subject):
        """Xoá Subject (cả LEC và LAB của nó) ra khỏi semester."""
        if self.isHaveLecOrLab(subject, self.semester.getSubjects()):
            i = 0
            while i < len(self.semester.getSubjects()):
                if subject.getRegisterCode() == self.semester.getSubjects()[i].getRegisterCode():
                    cl = self.semester.getSubjects()[i].getColor()
                    cs4rsa_color.remove_color(cl)
                    self.semester.deleteSubject(self.semester.getSubjects()[i])
                    continue
                i+=1
        else:
            cs4rsa_color.remove_color(subject.getColor())
            self.semester.deleteSubject(subject)
            self.removeSel()

    def addSubject(self, subject: Subject):
        cl = cs4rsa_color.hex_code_colors()
        if self.isHaveLecOrLab(subject, self.SUBJECT_FOUND):
            for i in self.isHaveLecOrLab(subject, self.SUBJECT_FOUND):
                self.SUBJECT_FOUND[i].setColor(cl)
                sub = self.SUBJECT_FOUND[i]
                self.semester.addSubject(sub)
        else:
            subject.setColor(cl)
            self.semester.addSubject(subject)

    def afterDeleteSubject(self, subject: Subject):
        self.loadListSubjectChoiced()
        self.loadListConflict()
        self.loadButtonWeekContainer(self.semester.getMaxWeekInSemester())
        if self.semester.getSubjects():
            self.loadTable(self.semester.getCurrentSubjects())
        else:
            self.resetColorTable()
        self.loadLabelWeek()
        self.enableItemInListFound(subject)

    def afterAddSubject(self):
        self.loadListSubjectChoiced()
        self.loadListConflict()
        self.loadButtonWeekContainer(self.semester.getMaxWeekInSemester())
        self.loadTable(self.semester.getCurrentSubjects())
        self.loadLabelWeek()
        self.unableItemInListFound()

    def register(self):
        print('Run register window')

    def updateSubject(self):
        # tạm thời update mình sẽ xoá tất cả mọi file trong thư mục data để nó tải lại mọi thứ.
        try:
            mss = QMessageBox.warning(
                self,
                team_config.MESSAGE_WARNING,
                team_config.MESSAGE_UPDATE_CONTENT,
                QMessageBox.Ok |
                QMessageBox.Cancel,
                defaultButton=QMessageBox.Cancel
            )
            if mss == QMessageBox.Ok:
                filelist = [ f for f in os.listdir(team_config.FOLDER_SAVE_EXCEL) if f.endswith(".xls") ]
                for f in filelist:
                    os.remove(os.path.join(team_config.FOLDER_SAVE_EXCEL, f))
                self.listView_SubjectDownloaded.clear()
        except:
            QMessageBox.warning(
                self,
                team_config.MESSAGE_WARNING,
                'Có vẻ như gặp lỗi trong quá trình cập nhật.')

    def fillDataToSubjectFound(self, subjects: List[Subject]):
        """Phương thức này nhận vào một JSON và render ra UI trên phần 
        Subject found."""
        self.listView_SubjectDownloaded.clear()
        self.SUBJECT_FOUND = subjects
        self.loadListSubjectFound()
        self.unableItemInListFound()
        
    def fillDataToSubjectFoundFromJsonFile(self, filename):
        """Phương thức này nhận vào một JSON file path và render ra UI trên phần 
        Subject found."""
        pass

    def findSubject(self, discipline, keyword1):
        """Tìm kiếm môn học."""
        loadingContents = ['🔍Đang tìm kiếm',
                            '🔎Đang tìm kiếm.',
                            '🔍Đang tìm kiếm..',
                            '🔎Đang tìm kiếm...',
                            '🔍Đang tìm kiếm....',
                            '🔎Đang tìm kiếm.....']
        self.loading = ThreadShowLoading(0.3, loadingContents)
        self.loading.signal_changeTitle.connect(lambda content: self.changeWindowTitle(content))
        self.loading.signal_stopLoading.connect(lambda content: self.changeWindowTitle('<i>{0}</i>'.format(content)))
        self.loading.start()

        contentSpecialSubject = """Có vẻ {0} là một môn học đặc biệt, app của bọn mình sẽ không xử lý những môn học như này.
                    <br>
                    <br>
                    <b>Môn học đặc biệt</b> là một môn mà có các nhóm lớp, trong mỗi nhóm lớp
                    như thế lại có nhiều mã đăng ký lớp học, những môn như thế sẽ được bọn mình bỏ qua vì thông thường
                    để đăng ký một lớp (hay đúng hơn là một nhóm lớp) các bạn chỉ cần 1 mã đăng ký.
                    <br>
                    <br>
                    <i style="font-size: 18px;">*Nguồn donate từ các bạn sẽ tạo động lực cho team nghiên cứu những môn như này. Cảm ơn.</i>"""
        contentNotFoundSubject = 'Có vẻ như {0} không tồn tại 😢😢😢'
        contentHaveNotSchedule = 'Không có lịch của môn {0} trong học kỳ này.'

        notiSpecialSubject = lambda subjectCode: NotificationWindow('Thông báo',contentSpecialSubject.format(subjectCode)).exec_()
        notiNotFoundSubject = lambda subjectCode: NotificationWindow('Thông báo',contentNotFoundSubject.format(subjectCode)).exec_()
        notiHaveNotSchedule = lambda subjectCode: NotificationWindow('Thông báo',contentHaveNotSchedule.format(subjectCode)).exec_()   
        
        def innerCleanWindowTitleAndNoti(noti, contentNoti: str):
            self.loading.stopLoading(contentNoti)
            noti(contentNoti)
            self.resetWindowTitle()
            self.line_findSubject.clear()
            self.line_findSubject.setFocus()

        currentSemesterValue = HomeCourseSearch.getCurrentSemesterValue()
        print('find', currentSemesterValue)
        self.threadDownloadSubject = ThreadDownloadSubject(currentSemesterValue, discipline, keyword1)
        self.threadDownloadSubject.signal_foundSubject.connect(self.fillDataToSubjectFound)
        self.threadDownloadSubject.signal_subjectName.connect(lambda content: self.loading.stopLoading(content))
        self.threadDownloadSubject.signal_notFoundSubject.connect(lambda content: innerCleanWindowTitleAndNoti(notiNotFoundSubject, content))
        self.threadDownloadSubject.signal_notHaveSchedule.connect(lambda content: innerCleanWindowTitleAndNoti(notiHaveNotSchedule, content))
        self.threadDownloadSubject.signal_specialSubject.connect(lambda content: innerCleanWindowTitleAndNoti(notiSpecialSubject, content))
        self.threadDownloadSubject.start()

    # Các phương thức thao tác trên Table và các thành phần giao diện khác
    def resetColorTable(self):
        for i in range(self.table_Semeter.rowCount()):
            for c in range(self.table_Semeter.columnCount()):
                self.table_Semeter.setItem(i, c, QTableWidgetItem())
                self.table_Semeter.item(i, c).setBackground(QColor(255,255,255))

    def paintConflict(self) -> List[str]:
        """Vẽ Conflict lên bảng."""
        if len(self.semester.getCurrentSubjects()) >= 2:
            for conflictsASubject in self.semester.scanSubjectConflict():
                for conflict in conflictsASubject:
                    key = next(iter(conflict))
                    col = self.semester.DATE_CHAINS[key]
                    startConflict = self.semester.TIME_CHAINS[conflict[key][0]]
                    endConflict = self.semester.TIME_CHAINS[conflict[key][1]]
                    for row in range(startConflict, endConflict+1):
                        item = QTableWidgetItem()
                        item.setText('Conflict')
                        item.setBackground(QColor('#FF0000'))
                        self.table_Semeter.setItem(row, col, item)

    def removeSel(self):
        """Xoá Subject đã chọn khỏi listView_SubjectChoiced"""
        listItems=self.listView_SubjectChoiced.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.listView_SubjectChoiced.takeItem(self.listView_SubjectChoiced.row(item))

    def unableItemInListFound(self):
        """Ẩn hoặc vô hiệu Subject đã thêm vào bảng."""
        setSubjectChoicedIDs = {subject.getRegisterCode() for subject in self.semester.getSubjects()}
        for i in range(self.listView_SubjectDownloaded.count()):
            if self.listView_SubjectDownloaded.item(i).data(Qt.UserRole).getRegisterCode() in setSubjectChoicedIDs:
                self.listView_SubjectDownloaded.item(i).setHidden(True)

    def enableItemInListFound(self, subject: Subject):
        """Hiển thị Subject đã thêm vào bảng."""
        for i in range(self.listView_SubjectDownloaded.count()):
            if self.listView_SubjectDownloaded.item(i).data(Qt.UserRole).getRegisterCode() == subject.getRegisterCode():
                self.listView_SubjectDownloaded.item(i).setHidden(False)

    # Navigation in Semester
    def gotoPreviousWeek(self):
        """Điều hướng tới Tuần trước của Semester."""
        self.semester.previousWeek()
        self.loadTable(self.semester.getCurrentSubjects())
        self.loadLabelWeek()

    def gotoNextWeek(self):
        """Điều hướng tới Tuần kế tiếp của Semester."""
        self.semester.nextWeek()
        self.loadTable(self.semester.getCurrentSubjects())
        self.loadLabelWeek()

    def gotoWeek(self, week):
        self.semester.gotoWeek(week)
        self.loadTable(self.semester.getCurrentSubjects())
        self.loadLabelWeek()

    # Các phương thức kiểm tra và logic
    def isHaveLecOrLab(self, subject: Subject, inList: list) -> List:
        """Kiểm tra List of Subject truyền vào có Môn LEC hay LAB hay không. 
        Nếu có trả về list index của Subject LEC hoặc LAB tương ứng. Nếu không trả về None."""
        output = []
        i = 0
        while i<len(inList):
            if subject.getRegisterCode() == inList[i].getRegisterCode():
                output.append(i)
            i+=1
        return output


    # Giao diện
    def closeWindow(self):
        self.close()

    def minimum(self):
        self.showMinimized()

    def maximum(self):
        if self.WINDOW_IS_MAXIMIZED:
            width = (QDesktopWidget().size().width()/100)*80
            height = (QDesktopWidget().size().height()/100)*80
            centerPoint = QDesktopWidget().availableGeometry().center()
            self.hopePointX = centerPoint.x() - width/2
            self.hopePointY = centerPoint.y() - height/2
            self.qrect = QRect(self.hopePointX, self.hopePointY, width, height)
            self.ani = QPropertyAnimation(self, b'geometry')
            self.ani.setDuration(300)
            self.ani.setEndValue(self.qrect)
            self.ani.setEasingCurve(QEasingCurve.InOutQuad)
            self.ani.start()
            self.WINDOW_IS_MAXIMIZED = False
        else:
            self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            self.screenRect.setHeight(self.screenRect.height()-50)
            self.ani = QPropertyAnimation(self, b'geometry')
            self.ani.setDuration(300)
            self.ani.setEndValue(self.screenRect)
            self.ani.setEasingCurve(QEasingCurve.InOutQuad)
            self.ani.start()
            self.WINDOW_IS_MAXIMIZED = True

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.moving:
            self.move(event.globalPos()-self.offset)

    def expandNavbar(self):
        init_frame_navi_width = self.frame_navi.width()
        if init_frame_navi_width == 60:
            newWidth = 200
        else:
            newWidth = 60
        self.aniNav = QPropertyAnimation(self.frame_navi, b'minimumWidth')
        self.aniNav.setDuration(300)
        self.aniNav.setStartValue(init_frame_navi_width)
        self.aniNav.setEndValue(newWidth)
        self.aniNav.setEasingCurve(QEasingCurve.InOutQuart)
        self.aniNav.start()


    def changeWindowTitle(self, title):
        newTitle = self.dynamicTitle+' • {0}'.format(title)
        self.label_windowTitle.setText(newTitle)

    def resetWindowTitle(self):
        self.label_windowTitle.setText(self.dynamicTitle)

    def selectAllAndFocusFindQLineEdit(self):
        self.line_findSubject.setFocus()
        self.line_findSubject.selectAll()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
    
