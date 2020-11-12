from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic

from class_weeksChoicer import WeeksChoicer
from class_customwidget import QCustomQWidget
from class_customConflictWidget import CustomConflictWidget
from class_semester import *
from class_subject import Subject
from class_schedule import StringToSchedule
from class_calendar import *
from class_convertType import *

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
        self.semester = Semester()
        self.calendar = None
        uic.loadUi(team_config.FOLDER_UI+'/'+team_config.USE_UI, self)

        self.button_findSubject = ConvertThisQObject(self, QPushButton, 'pushButton_timKiem').toQPushButton()
        self.button_updateSubject = ConvertThisQObject(self, QPushButton, 'pushButton_capNhat').toQPushButton()
        self.button_deleleSubjectFromTable = ConvertThisQObject(self, QPushButton, 'pushButton_xoaLop').toQPushButton()
        self.button_saveExcel = ConvertThisQObject(self, QPushButton, 'pushButton_luuText').toQPushButton()
        self.button_nextWeek = ConvertThisQObject(self, QPushButton, 'pushButton_nextWeek').toQPushButton()
        self.button_previousWeek = ConvertThisQObject(self, QPushButton, 'pushButton_previousWeek').toQPushButton()
        self.button_gotoWeek = ConvertThisQObject(self, QPushButton, 'pushButton_goto').toQPushButton()

        self.listView_SubjectDownloaded = ConvertThisQObject(self, QListWidget, 'listWidget_tenLop').toQListWidget()
        self.listView_SubjectChoiced = ConvertThisQObject(self, QListWidget, 'listWidget_lopDaChon').toQListWidget()
        self.listView_SubjectConflict = ConvertThisQObject(self, QListWidget, 'listWidget_lopXungDot').toQListWidget()

        self.line_findSubject = ConvertThisQObject(self, QLineEdit, 'lineEdit_tenMon').toQLineEdit()

        self.checkBox_phase1 = ConvertThisQObject(self, QCheckBox, 'checkBox_giaiDoan1').toQCheckBox()
        self.checkBox_phase2 = ConvertThisQObject(self, QCheckBox, 'checkBox_giaiDoan2').toQCheckBox()

        self.textEdit_thongtin = ConvertThisQObject(self, QTextEdit, 'textEdit_thongtin').toQTextEdit()
        self.textEdit_thongke = ConvertThisQObject(self, QTextEdit, 'textEdit_thongke').toQTextEdit()

        self.table_Semeter = ConvertThisQObject(self, QTableWidget, 'tableWidget_lichHoc').toQTableWidget()

        self.connectSignals()
        self.addShortcut()

    def connectSignals(self):
        """Phương thức này kết nối signal với slot tương ứng."""
        self.button_findSubject.clicked.connect(self.findSubject)
        self.button_deleleSubjectFromTable.clicked.connect(self.deleteSubject)
        self.button_updateSubject.clicked.connect(self.updateSubject)
        self.button_gotoWeek.clicked.connect(self.showWeeks)
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
                    start_row = self.semester.getTimeChains()[start]
                    end_row = self.semester.getTimeChains()[end]
                    column = WEEK.index(day)
                    for pen in range(start_row, end_row+1):
                        item = QTableWidgetItem()
                        item.setText(subject.getName())
                        item.setBackground(color)
                        item.setToolTip(subject.getFullName())
                        self.table_Semeter.setItem(pen, column, item)
        self.paintConflict()


    def deleteSubject(self):
        """Xoá Subject (cả LEC và LAB của nó) ra khỏi semester."""
        item = self.listView_SubjectChoiced.currentItem()
        if item:
            subject = item.data(Qt.UserRole) # subject được chọn trong QListWidget
            if self.checkLecLab(subject, self.semester.getSubjectsInSemester()):
                i = 0
                while i < len(self.semester.getSubjectsInSemester()):
                    if subject.getID() == self.semester.getSubjectsInSemester()[i].getID():
                        # Xoá trên semester
                        self.semester.deleteSubject(self.semester.getSubjectsInSemester()[i].getName())
                        continue
                    i+=1
            else:
                self.semester.deleteSubject(subject.getName())
                self.removeSel()
            self.loadTable(self.semester.getSubjectsInSemester())
            self.loadListChoosed()
            self.checkEnableItemInListFound(subject)
        else:
            QMessageBox.warning(self,
                'Một thông báo sương sương',
                'Vui lòng chọn một môn nào đó để xoá khỏi lịch. Bạn có thể Donate để mở khoá tính năng xoá một lúc nhiều môn.',
                QMessageBox.Ok)


    def removeSel(self):
        """Xoá Subject đã chọn khỏi listView_SubjectChoiced"""
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
                filelist = [ f for f in os.listdir(team_config.FOLDER_SAVE_EXCEL) if f.endswith(".xls") ]
                for f in filelist:
                    os.remove(os.path.join(team_config.FOLDER_SAVE_EXCEL, f))
        except:
            QMessageBox.warning(
                self,
                team_config.MESSAGE_WARNING,
                'Có vẻ như gặp lỗi trong quá trình cập nhật.')

    def checkLecLab(self, subject: Subject, inList: list) -> List:
        """Kiểm tra Subject truyền vào có Môn LEC hay LAB hay không. 
        Nếu có trả về list index của Subject LEC hoặc LAB tương ứng. N
        ếu không trả về None."""
        output = []
        i = 0
        while i<len(inList):
            if subject.getID() == inList[i].getID():
                output.append(i)
            i+=1
        return output


    def addSubjectToTable(self, subject: Subject=None):
        cl = color.getColor()
        if self.checkLecLab(subject, self.SUBJECT_FOUND):
            for i in self.checkLecLab(subject, self.SUBJECT_FOUND):
                self.SUBJECT_FOUND[i].setColor(cl)
                sub = self.SUBJECT_FOUND[i]
                self.semester.addSubjectToSemester(sub)
        else:
            subject.setColor(cl)
            self.semester.addSubjectToSemester(subject)
        self.loadListChoosed()
        self.loadTable(self.semester.getSubjectsInSemester())
        self.checkUnableItemInListFound()

    def afterAddSubject(self):
        """Hàm này chạy bất cứ khi nào bạn Add một Subject vào Semester. 
        Dùng để load lại giao diện cho đúng logic."""
        pass

    def checkUnableItemInListFound(self):
        """Ẩn hoặc vô hiệu Subject đã thêm vào bảng."""
        setSubjectChoicedIDs = {i.getID() for i in self.semester.getSubjectsInSemester()}
        for i in range(self.listView_SubjectDownloaded.count()):
            if self.listView_SubjectDownloaded.item(i).data(Qt.UserRole).getID() in setSubjectChoicedIDs:
                self.listView_SubjectDownloaded.item(i).setHidden(True)

    def checkEnableItemInListFound(self, subject: Subject):
        """Ẩn hoặc vô hiệu Subject đã thêm vào bảng."""
        for i in range(self.listView_SubjectDownloaded.count()):
            if self.listView_SubjectDownloaded.item(i).data(Qt.UserRole).getID() == subject.getID():
                self.listView_SubjectDownloaded.item(i).setHidden(False)

    def paintConflict(self) -> List[str]:
        """Vẽ Conflict lên bảng."""
        if len(self.semester.getSubjectsInSemester()) >= 2:
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
        self.loadListConflict()

    def loadListConflict(self):
        """Load List Widget chứa thông tin Subject Conflict."""
        self.listView_SubjectConflict.clear()
        for conflict in self.semester.scanConflicts():
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
        self.loadListSubjectFound()


    def loadListChoosed(self):
        print('choice', self.semester.getSubjectsInSemester())
        self.listView_SubjectChoiced.clear()
        for subject in self.semester.getSubjectsInSemester():

            self.custom_widget_subject = QCustomQWidget(subject)
            self.custom_widget_subject.addButtonCopyIDSubject()

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectChoiced)
            self.myQListWidgetItem.setData(Qt.UserRole, subject)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())

            self.listView_SubjectChoiced.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)
            self.listView_SubjectChoiced.addItem(self.myQListWidgetItem)


    def loadListSubjectFound(self):
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


    def showWeeks(self):
        if self.semester.getMaxWeekInSemester() == 0:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setWindowTitle(team_config.MESSAGE_ABOUT)
            msgbox.setText('Có vẻ như bạn chưa thêm môn nào vào bảng. Hãy thử tìm kiếm và thêm ít nhất một môn vào bảng.')
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec()
            self.line_findSubject.setFocus()
            return
        weekChoicer = WeeksChoicer(self.semester.getMaxWeekInSemester())
        weekChoicer.exec()

    def fillCalendarToSemeter(self, e):
        print(e)

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
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.show()

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

    def showAboutUs(self):
        self.f = QWidget()
        uic.loadUi(r'GUI\about_us.ui', self.f)
        self.f.show()

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())