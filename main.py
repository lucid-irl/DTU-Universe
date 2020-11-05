from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic

from class_customwidget import QCustomQWidget
from class_customConflictWidget import CustomConflictWidget
from class_semeter import *
from class_subject import Subject
from class_schedule import StringToSchedule
from class_calendar import *

from thread_getSubject import ThreadGetSubject

import sys
import os
import xlrd
import color
import team_config
import sys

class Main(QMainWindow):
    """Class này chỉ đảm nhiệm việc xử lý giao diện."""

    SUBJECT_FOUND = []

    def __init__(self, mainwindow=None):
        super(Main, self).__init__()
        self.mainwindow = mainwindow
        self.semeter = Semeter()
        self.calendar = None
        uic.loadUi(team_config.FOLDER_UI+'/'+team_config.USE_UI, self)

        self.button_findSubject = self.findChild(QPushButton,'pushButton_timKiem')
        self.button_addSujectToTable = self.findChild(QPushButton, 'pushButton_themLop')
        self.button_updateSubject = self.findChild(QPushButton, 'pushButton_capNhat')
        self.button_deleleSubjectFromTable = self.findChild(QPushButton, 'pushButton_xoaLop')
        self.button_saveExcel = self.findChild(QPushButton, 'pushButton_luuText')
        self.button_choiceCalendar = self.findChild(QPushButton, 'pushButton_choiceCalendar')

        self.listView_SubjectDownloaded = self.findChild(QListWidget, 'listWidget_tenLop')
        self.listView_SubjectChoiced = self.findChild(QListWidget, 'listWidget_lopDaChon')
        self.listView_SubjectConflict = self.findChild(QListWidget, 'listWidget_lopXungDot')

        self.line_findSubject = self.findChild(QLineEdit, 'lineEdit_tenMon')

        self.checkBox_phase1 = self.findChild(QCheckBox, 'checkBox_giaiDoan1')
        self.checkBox_phase2 = self.findChild(QCheckBox, 'checkBox_giaiDoan2')

        self.textEdit_thongtin = self.findChild(QTextEdit, 'textEdit_thongtin')
        self.textEdit_thongke = self.findChild(QTextEdit, 'textEdit_thongke')

        self.table_Semeter = self.findChild(QTableWidget, 'tableWidget_lichHoc')

        # self.show()
        self.addSignalWidget()
        self.addShortcut()

################## hot fix ##################################
        # self.button_findSubject = QPushButton()
        # self.button_addSujectToTable = QPushButton()
        # self.button_updateSubject = QPushButton()
        # self.button_deleleSubjectFromTable = QPushButton()
        # self.button_saveExcel = QPushButton()
        # self.button_choiceCalendar = QPushButton()

        # self.listView_SubjectDownloaded = QListWidget()
        # self.listView_SubjectChoiced = QListWidget()
        # self.listView_SubjectConflict = QListWidget()

        # self.line_findSubject = QLineEdit()

        # self.checkBox_phase1 = QCheckBox()
        # self.checkBox_phase2 = QCheckBox()

        # self.textEdit_thongtin = QTextEdit()

        # self.table_Semeter = QTableWidget()
################## hot fix ##################################



    def addSignalWidget(self):
        """Phương thức này kết nối signal với slot tương ứng."""
        self.button_findSubject.clicked.connect(self.findSubject)
        self.button_deleleSubjectFromTable.clicked.connect(self.deleteSubject)
        self.button_updateSubject.clicked.connect(self.updateSubject)
        self.button_choiceCalendar.clicked.connect(self.openCalendarChoicer)
        self.listView_SubjectDownloaded.itemClicked.connect(self.showInfoSubject)
        self.listView_SubjectChoiced.itemClicked.connect(self.showInfoSubject)

    def addShortcut(self):
        """Phương thức này chịu trách nhiệm gán Shortcut cho các chức năng trong ứng dụng."""
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(QApplication.instance().quit)
        
        # shortcut for button here
        self.button_findSubject.setShortcut('Return')

    def loadTable(self, subjects: List[Subject]):
        self.resetColorTable()
        for subject in subjects:
            days = subject.getSchedule().getDatesOfLesson()
            color = QColor(subject.getColor())
            for day in days:
                start_time_subjects = subject.getSchedule().getStartTimeOfDate(day)
                end_time_subjects = subject.getSchedule().getEndTimeOfDate(day)
                for i in range(len(start_time_subjects)):
                    start = str(start_time_subjects[i])
                    end = str(end_time_subjects[i])
                    start_row = self.semeter.getTimeChains()[start]
                    end_row = self.semeter.getTimeChains()[end]
                    column = WEEK.index(day)
                    for pen in range(start_row, end_row+1):
                        item = QTableWidgetItem()
                        item.setText(subject.getName())
                        item.setBackground(color)
                        item.setToolTip(subject.getFullName())
                        self.table_Semeter.setItem(pen, column, item)


    def deleteSubject(self):
        item = self.listView_SubjectChoiced.currentItem()
        if item:
            subject = item.data(Qt.UserRole)
            self.semeter.deleteSubject(subject.getName())
            self.removeSel()
            self.loadTable(self.semeter.getSubjectsInSemeter())
        else:
            QMessageBox.warning(self,
                'Một thông báo sương sương',
                """Vui lòng chọn một môn nào đó để xoá khỏi lịch. Bạn có thể Donate để mở khoá tính năng xoá một lúc nhiều môn.""",
                QMessageBox.Ok)


    def removeSel(self):
        listItems=self.listView_SubjectChoiced.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.listView_SubjectChoiced.takeItem(self.listView_SubjectChoiced.row(item))

    
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
                print('OK')
                filelist = [ f for f in os.listdir(team_config.FOLDER_SAVE_EXCEL) if f.endswith(".xls") ]
                for f in filelist:
                    os.remove(os.path.join(team_config.FOLDER_SAVE_EXCEL, f))
        except:
            QMessageBox.warning(
                self,
                team_config.MESSAGE_WARNING,
                'Có vẻ như gặp lỗi trong quá trình cập nhật.')


    def addSubjectToTable(self, subject: Subject=None):
        subject.setColor(color.getColor())
        self.semeter.addSubjectToSemeter(subject)
        self.loadListChoosed()
        self.loadTable(self.semeter.getSubjectsInSemeter())
        self.paintConflict()


    def paintConflict(self) -> List[str]:
        if len(self.semeter.getSubjectsInSemeter()) >= 2:
            for conflictsASubject in self.semeter.scanSubjectConflict():
                for conflict in conflictsASubject:
                    key = next(iter(conflict))
                    col = self.semeter.DATE_CHAINS[key]
                    startConflict = self.semeter.TIME_CHAINS[conflict[key][0]]
                    endConflict = self.semeter.TIME_CHAINS[conflict[key][1]]
                    for row in range(startConflict, endConflict+1):
                        item = QTableWidgetItem()
                        item.setText('Conflict')
                        item.setBackground(QColor('#FF0000'))
                        self.table_Semeter.setItem(row, col, item)
        self.loadListConflict()

    def loadListConflict(self):
        self.listView_SubjectConflict.clear()
        for conflict in self.semeter.scanConflicts():
            sub1 = conflict.getSubject1()
            sub2 = conflict.getSubject2()

            self.custom_conflict_widget = CustomConflictWidget(sub1, sub2)

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectConflict)
            self.myQListWidgetItem.setData(Qt.UserRole, conflict)
            self.myQListWidgetItem.setSizeHint(self.custom_conflict_widget.sizeHint())

            self.listView_SubjectConflict.setItemWidget(self.myQListWidgetItem, self.custom_conflict_widget)
            self.listView_SubjectConflict.addItem(self.myQListWidgetItem)


    def findSubject(self):
        self.SUBJECT_FOUND.clear()
        self.listView_SubjectDownloaded.clear()
        self.textEdit_thongtin.clear()
        self.textEdit_thongtin.setText('Đang tìm kiếm...')
        subject_name = self.line_findSubject.text()
        file_name = team_config.FOLDER_SAVE_EXCEL+'/'+subject_name+'.xls'

        self.thread_getsubject = ThreadGetSubject(subject_name)
        self.thread_getsubject.signal_foundExcel.connect(self.fillDataToSubjects)
        self.thread_getsubject.signal_nonFoundExcel.connect(self.nonFoundSubject)
        if os.path.exists(file_name):
            self.fillDataToSubjects(file_name)
        else:
            self.thread_getsubject.start()


    def fillDataToSubjects(self, e):
        self.textEdit_thongtin.clear()
        wb = xlrd.open_workbook(e)
        sheet = wb.sheet_by_index(0)
        
        for i in range(1, sheet.nrows):
            id = sheet.cell_value(i, 1)
            name = sheet.cell_value(i, 2)
            schedule = StringToSchedule(sheet.cell_value(i, 3))
            place = sheet.cell_value(i, 4)
            teacher = sheet.cell_value(i, 5)
            credit = int(sheet.cell_value(i, 6))
            seats = sheet.cell_value(i, 7)
            week_range = sheet.cell_value(i, 8).split('--')
            status =  int(sheet.cell_value(i, 9))
            fullname = sheet.cell_value(i, 10)
            subject = Subject(id, name, seats, credit, schedule, teacher, place, week_range, status, fullname)
            self.SUBJECT_FOUND.append(subject)
        self.loadListView()


    def loadListChoosed(self):
        self.listView_SubjectChoiced.clear()
        for subject in self.semeter.getSubjectsInSemeter():

            self.custom_widget_subject = QCustomQWidget(subject)
            self.custom_widget_subject.addButtonCopyIDSubject()

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectChoiced)
            self.myQListWidgetItem.setData(Qt.UserRole, subject)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())

            self.listView_SubjectChoiced.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)
            self.listView_SubjectChoiced.addItem(self.myQListWidgetItem)


    def loadListView(self):
        for subject in self.SUBJECT_FOUND:
            self.custom_widget_subject = QCustomQWidget(subject, self)
            self.custom_widget_subject.addButtonAddToSemeter()

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectDownloaded)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())
            self.myQListWidgetItem.setData(Qt.UserRole, subject)

            self.listView_SubjectDownloaded.addItem(self.myQListWidgetItem)
            self.listView_SubjectDownloaded.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)


    def resetColorTable(self):
        for i in range(self.table_Semeter.rowCount()):
            for c in range(self.table_Semeter.columnCount()):
                self.table_Semeter.setItem(i, c, QTableWidgetItem())
                self.table_Semeter.item(i, c).setBackground(QColor(255,255,255))


    def showInfoSubject(self, e):
        self.textEdit_thongtin.clear()
        subject = e.data(Qt.UserRole)
        self.textEdit_thongtin.setText(subject.getInfo())

    def openCalendarChoicer(self):
        if self.calendar == None:
            self.calendar = CalendarChoicer()
        # active this window
        self.calendar.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.calendar.show()

    def nonFoundSubject(self):
        QMessageBox.warning(
            self, 
            team_config.MESSAGE_ABOUT,
            team_config.MESSAGE_DONATE_CONTENT,
            QMessageBox.Ok
        )

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(team_config.TITLE)
        self.setupUI()

    def setupUI(self):
        self.widget = Main(mainwindow=self)
        self.setCentralWidget(self.widget)
        # menu here
        self.menubar = QMenuBar(self.widget)
        self.menu_file = QMenu('Tệp tin', self.menubar)
        self.action_setting = QAction('Cài đặt')
        self.menu_file.addAction(self.action_setting)
        self.menu_help = QMenu('Trợ giúp', self.menubar)
        self.action_aboutUs = QAction('Về chúng tôi')
        self.action_aboutUs.triggered.connect(self.showAboutUs)
        self.menu_help.addAction(self.action_aboutUs)

        self.menubar.addMenu(self.menu_file)
        self.menubar.addMenu(self.menu_help)
        self.setMenuBar(self.menubar)
        # status bar
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.show()

    def showAboutUs(self):
        self.f = QWidget()
        uic.loadUi(r'GUI\about_us.ui', self.f)
        self.f.show()

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())