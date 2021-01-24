from PyQt5.QtWidgets import (QCheckBox, QShortcut, QStackedWidget, QWidget, QApplication, QPushButton, QListWidget, QListWidgetItem,
                            QTableWidget, QTableWidgetItem, QLineEdit, QLabel, 
                            QFrame, QScrollArea, QCompleter, QDesktopWidget)
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QColor, QIcon, QKeySequence, QValidator 
from PyQt5 import uic

from class_conflict import Conflict
from class_register import SubjectRegister
from class_dialogDonate import DonateWindow
from class_custom_list_item_widget import CustomListItemWidget
from class_customConflictWidget import CustomConflictWidget
from class_semester import Semester, WEEK
from class_subject import Subject
from class_convertType import ConvertThisQObject
from class_flow_layout import FlowLayout
from class_subjectCrawler import *
from class_dialogNotification import NotificationWindow
from class_homeCourseSearch import HomeCourseSearch
from class_setting import ConnectSettingToWidget, Setting
from class_detailSubjectTable import DetailSubjectWindow
from class_saveExcel import SaveExcel
from thread_downloadSubject import ThreadDownloadSubject, ThreadShowLoading

from typing import List

import logging
import sys
import cs4rsa_color
import team_config

logging.basicConfig(level=logging.DEBUG)
class ValidatorFindLineEdit(QValidator):
    """In hoa mọi ký tự nhập vào QLineEdit."""
    def validate(self, string, pos):
        return QValidator.Acceptable, string.upper(), pos

class Main(QWidget):
    """Class này chỉ đảm nhiệm việc xử lý giao diện."""

    SUBJECT_FOUND:List[Subject] = []
    CURRENT_SUBJECT:str = ''
    WINDOW_IS_MAXIMIZED = False
    # Chứa các cửa sổ giao diện thông tin chi tiết của một Subject
    WINDOW_DETAIL_INFO = None

    # Các phương thức setting Giao diện bao gồm kết nối Signal, add Hot key,...
    def __init__(self):
        super(Main, self).__init__() #Main, self
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.semester = Semester()
        self.setWindowIcon(QIcon('Images/new-logo.png'))
        self.currentSchoolYearValue = HomeCourseSearch.getCurrentSchoolYearValue()
        self.currentSemesterValue = HomeCourseSearch.getCurrentSemesterValue()
        uic.loadUi(team_config.UI_MAIN, self)

        self.button_findSubject = ConvertThisQObject(self, QPushButton, 'button_timKiem').toQPushButton()
        self.button_updateSubject = ConvertThisQObject(self, QPushButton, 'button_capNhat').toQPushButton()
        self.button_register = ConvertThisQObject(self, QPushButton, 'button_dangKy').toQPushButton()
        self.button_saveExcel = ConvertThisQObject(self, QPushButton, 'button_luuText').toQPushButton()
        self.button_nextWeek = ConvertThisQObject(self, QPushButton, 'button_nextWeek').toQPushButton()
        self.button_previousWeek = ConvertThisQObject(self, QPushButton, 'button_previousWeek').toQPushButton()
        self.button_gotoWeek = ConvertThisQObject(self, QPushButton, 'button_goto').toQPushButton()
        self.button_info = ConvertThisQObject(self, QPushButton, 'button_info').toQPushButton()

        # title bar
        self.button_close = ConvertThisQObject(self, QPushButton, 'button_close').toQPushButton()
        self.button_maximum = ConvertThisQObject(self, QPushButton, 'button_maximum').toQPushButton()
        self.button_minimum = ConvertThisQObject(self, QPushButton, 'button_minimum').toQPushButton()

        # navigation bar
        self.stackedWidget = ConvertThisQObject(self, QStackedWidget, 'stackedWidget').toQStackedWidget()
        self.stackedWidget.setCurrentIndex(0)

        self.frame_navi = ConvertThisQObject(self, QFrame, 'frame_navbar').toQFrame()
        self.button_menu = ConvertThisQObject(self, QPushButton, 'button_menu').toQPushButton()
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

        # frame setting
        self.label_setting = ConvertThisQObject(self, QLabel, 'label_setting').toQLabel()
        self.checkBox_setting_save_class = ConvertThisQObject(self, QCheckBox, 'checkBox_setting_save_class').toQCheckBox()
        self.checkBox_setting_auto_import_class = ConvertThisQObject(self, QCheckBox, 'checkBox_setting_auto_import_class').toQCheckBox()
        self.checkBox_setting_darkmode = ConvertThisQObject(self, QCheckBox, 'checkBox_setting_darkmode').toQCheckBox()
        self.checkBox_setting_show_info_when_hover = ConvertThisQObject(self, QCheckBox, 'checkBox_setting_show_info_when_hover').toQCheckBox()
        self.checkBox_setting_show_teacher_name = ConvertThisQObject(self, QCheckBox, 'checkBox_setting_show_teacher_name').toQCheckBox()
        self.checkBox_setting_show_date_conflict = ConvertThisQObject(self, QCheckBox, 'checkBox_setting_show_date_conflict').toQCheckBox()
        self.checkBox_setting_highlight_conflict = ConvertThisQObject(self, QCheckBox, 'checkBox_setting_highlight_conflict').toQCheckBox()
        self.button_setting_save = ConvertThisQObject(self, QPushButton, 'button_setting_save').toQPushButton()
        self.button_setting_default = ConvertThisQObject(self, QPushButton, 'button_setting_default').toQPushButton()

        self.setting = Setting('cs4rsa_settings.json')
        self.connectSetting = ConnectSettingToWidget(self.setting)
        self.connectSetting.connectSettingToWidget('system','saveChoicedSubject', self.checkBox_setting_save_class)
        self.connectSetting.connectSettingToWidget('system','autoImportSubjectFile', self.checkBox_setting_auto_import_class)
        self.connectSetting.connectSettingToWidget('appearance','darkMode', self.checkBox_setting_darkmode)
        self.connectSetting.connectSettingToWidget('itemListWidget','showInfoWhenHover', self.checkBox_setting_show_info_when_hover)
        self.connectSetting.connectSettingToWidget('itemListWidget','showTeacherNameBySide', self.checkBox_setting_show_teacher_name)
        self.connectSetting.connectSettingToWidget('itemConflictListWidget','showDayConflict', self.checkBox_setting_show_date_conflict)
        self.connectSetting.connectSettingToWidget('buttonWeekContainer','highlightConflictWeekButton', self.checkBox_setting_highlight_conflict)
        self.connectSetting.whichIsDefaultSettingButton(self.button_setting_default)
        self.connectSetting.whichIsSaveButton(self.button_setting_save)
        self.connectSetting.run()

        #frame info
        self.button_info_donate_green = ConvertThisQObject(self, QPushButton, 'button_info_donate_green').toQPushButton()
        self.button_info_donate_red = ConvertThisQObject(self, QPushButton, 'button_info_donate_red').toQPushButton()

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
        self.button_register.clicked.connect(self.actionRegister)
        self.button_saveExcel.clicked.connect(self.actionExportExcel)
        self.button_info.clicked.connect(self.showDetailInfo)
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
        
        # semester
        self.semester.signal_indexChanged.connect(self.loadIndexChange)
        self.semester.signal_addSubject.connect(self.afterAddSubject)
        self.semester.signal_deleteSubject.connect(self.afterDeleteSubject)

        # setting
        self.connectSetting.signal_settingChange.connect(lambda value: self.changeSettingTitle(value))
        self.connectSetting.signal_settingSave.connect(lambda value: self.changeSettingTitle(value))

        # info
        self.button_info_donate_red.clicked.connect(self.showDonateDialog)
        self.button_info_donate_green.clicked.connect(self.showDonateDialog)


    def addShortcut(self):
        """Phương thức này chịu trách nhiệm gán Shortcut cho các chức năng trong ứng dụng."""
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.close)

        # shortcut for button here
        self.button_findSubject.setShortcut('Ctrl+F')
        self.button_maximum.setShortcut('F')

    # IMPORTANT!!!
    # chứa action

    def actionFindSubject(self):
        logging.info('Click find subject')
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
        logging.info('Click previous')
        self.gotoPreviousWeek()

    def actionGoToNextWeek(self):
        logging.info('Click next')
        self.gotoNextWeek()

    def actionChangeFrame(self, frameIndex):
        logging.info('Go to {0}'.format(frameIndex))
        if frameIndex != 2:
            self.connectSetting.run()
            self.changeSettingTitle(True)
        self.stackedWidget.setCurrentIndex(frameIndex)
        
    def actionExportExcel(self):
        if len(self.semester.getSubjects()):
            self.exportExcel(self.semester.getSubjects())
        else:
            NotificationWindow('Thông báo', 'Có vẻ như bạn chưa thêm môn nào cho nên không thể xuất Excel được!').exec()

    def actionRegister(self):
        if len(self.semester.getSubjects()):
            self.register()
        else:
            NotificationWindow('Thông báo', 'Có vẻ như bạn chưa thêm môn nào cho nên không thể đăng ký được.').exec()


    # IMPORTANT!!!
    # Các phương thức load giao diện quan trọng
    def loadTable(self, subjects: List[Subject]):
        logging.info('Table load {0}'.format(subjects))
        self.resetColorTable()
        if subjects:
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
                            item.setToolTip(subject.getSubjectCode() +' • '+ subject.getName())
                            self.table_Semeter.setItem(pen, column, item)
            if len(self.semester.getCurrentSubjects()) > 1:
                self.paintAllConflict(self.semester.getConflictsForWeek())
        else:
            self.resetColorTable()

    def loadListConflict(self, conflicts: List[Conflict]):
        """Load List Widget chứa thông tin Subject Conflict."""
        logging.debug('List Conflict load {0}'.format(conflicts))
        self.listView_SubjectConflict.clear()
        if conflicts:
            for conflict in conflicts:
                sub1 = conflict.getSubject1()
                sub2 = conflict.getSubject2()

                self.custom_conflict_widget = CustomConflictWidget(sub1, sub2)

                self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectConflict)
                self.myQListWidgetItem.setData(Qt.UserRole, conflict)
                self.myQListWidgetItem.setSizeHint(self.custom_conflict_widget.sizeHint())

                self.listView_SubjectConflict.setItemWidget(self.myQListWidgetItem, self.custom_conflict_widget)
                self.listView_SubjectConflict.addItem(self.myQListWidgetItem)

    def loadListSubjectChoiced(self, subjects: List[Subject]):
        """Phương thức này sẽ làm sạch danh sách môn đã chọn và tải lại nó từ list môn học hiện có trong Semester."""
        logging.info('Load list widget choiced subjects--> {0}'.format(subjects))
        self.listView_SubjectChoiced.clear()
        for subject in subjects:

            self.custom_widget_subject = CustomListItemWidget(subject)
            self.custom_widget_subject.removeWhenRightClick()
            self.custom_widget_subject.addButtonShowDetailInfo()
            self.custom_widget_subject.addButtonCopyIDSubject()
            self.custom_widget_subject.addButtonDelete()
            self.custom_widget_subject.signal_buttonDeleteIsPressed.connect(self.deleteSubject)

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectChoiced)
            self.myQListWidgetItem.setData(Qt.UserRole, subject)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())

            self.listView_SubjectChoiced.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)
            self.listView_SubjectChoiced.addItem(self.myQListWidgetItem)

    def loadListSubjectFound(self):
        logging.info('Load list widget found subjects--> {0}'.format(self.SUBJECT_FOUND))
        for subject in self.SUBJECT_FOUND:
            self.custom_widget_subject = CustomListItemWidget(subject, self)
            self.custom_widget_subject.addButtonShowDetailInfo()
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
            logging.info('clear flowlayout')
            self.flowlayout.clear()
        else:
            for index in range(maxWeek):
                self.weekButton = QPushButton(str(index+1), self)
                if index == self.semester.getCurrentSemesterIndex():
                    stylingString = """QPushButton {background-color: #2980b9;border-bottom: 5px solid #0a3d62;color: white;font-weight: bold;}
                    QPushButton:pressed {border:none;}"""
                    self.weekButton.setStyleSheet(stylingString)
                self.weekButton.setFixedWidth(40)
                self.weekButton.setFixedHeight(40)
                self.weekButton.clicked.connect(lambda b, value=index+1: self.gotoWeek(value))
                self.flowlayout.addWidget(self.weekButton)

    def loadLabelWeek(self):
        if self.semester.getSubjects():
            self.label_week.setText('Tuần '+str(self.semester.getCurrentSemesterIndex()+1))
        else:
            self.label_week.setText('Tuần ?')

    def loadIndexChange(self):
        self.loadButtonWeekContainer(self.semester.getMaxWeek())
        logging.info('loadTable --> {0}'.format(self.semester.getCurrentSubjects()))
        self.loadTable(self.semester.getCurrentSubjects())
        self.loadLabelWeek()

    # IMPORTANT!!!
    # Các phương thức thao tác trên Subject
    def deleteSubject(self, subject: Subject):
        """Xoá Subject (cả LEC và LAB của nó) ra khỏi semester."""
        logging.info('DELETE --> {0}'.format(subject))
        cs4rsa_color.remove_color(subject.getColor())
        self.semester.deleteSubject(subject)

    def addSubject(self, subject: Subject):
        """Thêm một Subject vào Semester."""
        logging.info('ADD --> {0}'.format(subject))
        cl = cs4rsa_color.generateRandomColor(255, 255, 255)
        subject.setColor(cl)
        self.semester.addSubject(subject)

    def afterDeleteSubject(self, subject: Subject):
        logging.info('after delete --> {0}'.format(subject))
        self.loadListSubjectChoiced(self.semester.getSubjects())
        self.loadListConflict(self.semester.getConflicts())
        self.loadButtonWeekContainer(self.semester.getMaxWeek())
        self.loadTable(self.semester.getCurrentSubjects())
        self.loadLabelWeek()
        self.showItemInListDownloadedAfterDelInListChoiced(subject)
        for detailWindow in Main.WINDOW_DETAIL_INFO:
            detailWindow.enableButtonAddSubject(subject)

    def afterAddSubject(self, subject: Subject):
        self.loadListSubjectChoiced(self.semester.getSubjects())
        self.loadListConflict(self.semester.getConflicts())
        self.loadButtonWeekContainer(self.semester.getMaxWeek())
        self.loadTable(self.semester.getCurrentSubjects())
        self.loadLabelWeek()
        self.hideItemIsHavedInListChoiced()

    def register(self):
        logging.info('Register run')
        registerClassCodes = []
        for i in range(self.listView_SubjectChoiced.count()):
            item = self.listView_SubjectChoiced.item(i)
            subject: Subject = item.data(Qt.UserRole)
            registerClassCodes.append(subject.getRegisterCode())
        logging.info('Register Class Codes {0}'.format(registerClassCodes))
        SubjectRegister(registerClassCodes, self.currentSemesterValue, self.currentSchoolYearValue, self).exec()

    @staticmethod
    def getSubjectsInListWidget(listWidget: QListWidget) -> List[Subject]:
        subjects = []
        for i in range(listWidget.count()):
            subject: Subject = listWidget.item(i).data(Qt.UserRole)
            subjects.append(subject)
        return subjects

    @staticmethod
    def getSubjectInListWidgetAtIndex(listWidget: QListWidget, index: int) -> Subject:
        return listWidget.item(index).data(Qt.UserRole)

    def fillDataToSubjectFound(self, subjectData: SubjectData):
        """Phương thức này nhận vào một SubjectData và render ra UI trên phần 
        Subject found."""
        self.subjectData = subjectData
        self.listView_SubjectDownloaded.clear()
        self.SUBJECT_FOUND = subjectData.getSubjects()
        self.loadListSubjectFound()
        self.hideItemIsHavedInListChoiced()

    def hideItemIsHavedInListChoiced(self):
        """Quét tất cả các phần từ có trong danh sách đã chọn, ẩn những phần tử có cùng mã môn với chúng."""
        logging.info('hideItemIsHavedInListChoiced run')
        for i in range(self.listView_SubjectChoiced.count()):
            subjectChoied:Subject = self.listView_SubjectChoiced.item(i).data(Qt.UserRole)
            for j in range(self.listView_SubjectDownloaded.count()):
                subjectDownloaded: Subject = self.listView_SubjectDownloaded.item(j).data(Qt.UserRole)
                if subjectChoied.getSubjectCode() == subjectDownloaded.getSubjectCode():
                    self.listView_SubjectDownloaded.item(j).setHidden(True)

    def showItemInListDownloadedAfterDelInListChoiced(self, subject: Subject):
        for i in range(self.listView_SubjectDownloaded.count()):
            downloadedSubject = Main.getSubjectInListWidgetAtIndex(self.listView_SubjectDownloaded, i)
            if subject.getSubjectCode() == downloadedSubject.getSubjectCode():
                self.listView_SubjectDownloaded.item(i).setHidden(False)

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
        self.threadDownloadSubject = ThreadDownloadSubject(currentSemesterValue, discipline, keyword1)
        self.threadDownloadSubject.signal_foundSubject.connect(self.fillDataToSubjectFound)
        self.threadDownloadSubject.signal_subjectName.connect(lambda content: self.loading.stopLoading(content))
        self.threadDownloadSubject.signal_notFoundSubject.connect(lambda content: innerCleanWindowTitleAndNoti(notiNotFoundSubject, content))
        self.threadDownloadSubject.signal_notHaveSchedule.connect(lambda content: innerCleanWindowTitleAndNoti(notiHaveNotSchedule, content))
        self.threadDownloadSubject.signal_specialSubject.connect(lambda content: innerCleanWindowTitleAndNoti(notiSpecialSubject, content))
        self.threadDownloadSubject.start()

    def showDetailInfo(self):
        logging.info('show detail subject info')
        if Main.WINDOW_DETAIL_INFO == None:
            Main.WINDOW_DETAIL_INFO:List[DetailSubjectWindow] = []
        detailInfo = DetailSubjectWindow(self, self.subjectData ,team_config.UI_DETAILSUBJECTTABLE, 
                                        'button_minimum','button_maximum','button_close','label_windowTitle')
        detailInfo.renderDetailTable()

        detailInfo.signal_addSubject.connect(lambda subject:self.addSubject(subject))
        Main.WINDOW_DETAIL_INFO.append(detailInfo)
        Main.WINDOW_DETAIL_INFO[-1].show()

        # cleaning the closed window
        # free mem
        i = 0
        while i < len(Main.WINDOW_DETAIL_INFO):
            if not Main.WINDOW_DETAIL_INFO[i].isVisible():
                Main.WINDOW_DETAIL_INFO.pop(i)
                continue
            i+=1

    def exportExcel(self, subjects: List[Subject]):
        self.saveExcelWindow = SaveExcel(team_config.UI_SAVE_EXCEL, 'button_minimum','button_maximum', 'button_close','label_windowTitle',subjects)
        self.saveExcelWindow.show()

    # Các phương thức thao tác trên Table và các thành phần giao diện khác
    def resetColorTable(self):
        """Xoá tất cả mọi thứ trên bảng."""
        for i in range(self.table_Semeter.rowCount()):
            for c in range(self.table_Semeter.columnCount()):
                self.table_Semeter.setItem(i, c, QTableWidgetItem())
                self.table_Semeter.item(i, c).setBackground(QColor(255,255,255))
    
    def paintAConflict(self, conflict: Conflict):
        """Vẽ một Conflict lên bảng."""
        logging.info('paint A Conflict {}'.format(conflict))
        for time in conflict.getConflictTime():
            key = next(iter(time))
            col = self.semester.DATE_CHAINS[key]
            startConflict = self.semester.TIME_CHAINS[time[key][0]]
            endConflict = self.semester.TIME_CHAINS[time[key][1]]
            for row in range(startConflict, endConflict+1):
                item = QTableWidgetItem()
                item.setText('{0}⚡{1}'.format(conflict.getSubject1().getSubjectCode(), conflict.getSubject2().getSubjectCode()))
                item.setBackground(QColor('#FF0000'))
                self.table_Semeter.setItem(row, col, item)

    def paintAllConflict(self, listConflict: List[Conflict]):
        """Vẽ tất cả Conflict lên bảng."""
        for conflict in listConflict:
            self.paintAConflict(conflict)


    def removeSel(self):
        """Xoá Subject đã chọn khỏi listView_SubjectChoiced"""
        listItems=self.listView_SubjectChoiced.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.listView_SubjectChoiced.takeItem(self.listView_SubjectChoiced.row(item))

# Navigation in Semester
    def gotoPreviousWeek(self):
        """Điều hướng tới Tuần trước của Semester."""
        logging.info('gotoPreviousWeek run')
        self.semester.previousWeek()

    def gotoNextWeek(self):
        """Điều hướng tới Tuần kế tiếp của Semester."""
        logging.info('gotoNextWeek run')
        self.semester.nextWeek()

    def gotoWeek(self, week):
        logging.info('gotoWeek {0} run'.format(week))
        self.semester.gotoWeek(week)

# Các phương thức kiểm tra và logic

    #setting


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

    # Giao diện phần setting
    def changeSettingTitle(self, value):
        self.label_setting.setTextFormat(Qt.RichText)
        if value:
            self.label_setting.setText('<html><head/><body><p>Cài đặt</p></body></html>')
        else:
            self.label_setting.setText('<html><head/><body><p>Cài đặt<span style=" vertical-align:super;">*</span></p></body></html>')

    def showDonateDialog(self):
        DonateWindow().exec()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        r = requests.get('https://www.google.com.vn/?hl=vi')
        window = Main()
        window.show()
        app.exec_()
    except:
        NotificationWindow('Thông tin', 'Có vẻ bạn chưa đóng tiền wifi hay sao đó mà đéo có mạng. Quay lại khi có mạng nhé.', 'Mình hiểu rồi huhu').exec()

    
