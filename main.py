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

    # Các phương thức setting Giao diện bao gồm kết nối Signal, add Hot key,...
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
        self.button_deleleSubjectFromTable.clicked.connect(self.actionDeleteSubject)
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


    # IMPORTANT!!!
    # Các phương thức này chuẩn bị đủ đúng context trước khi thao tác, ta gọi chúng là Action
    def actionDeleteSubject(self):
        """Action này được gọi khi người dùng định xoá một Subject ra khỏi Semester."""
        item = self.listView_SubjectChoiced.currentItem()
        if item:
            subject = item.data(Qt.UserRole)
            self.deleteSubject(subject)
        else:
            self.messageError()

    def actionFindSubject(self):
        pass


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
                        item.setText(subject.getName())
                        item.setBackground(color)
                        item.setToolTip(subject.getFullName())
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
            self.custom_widget_subject.signal_buttonAddIsPressed.connect(self.addSubject)

            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectDownloaded)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())
            self.myQListWidgetItem.setData(Qt.UserRole, subject)

            self.listView_SubjectDownloaded.addItem(self.myQListWidgetItem)
            self.listView_SubjectDownloaded.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)


    # IMPORTANT!!!
    # Các phương thức thao tác trên Subject
    def deleteSubject(self, subject: Subject):
        """Xoá Subject (cả LEC và LAB của nó) ra khỏi semester."""
        if self.isHaveLecOrLab(subject, self.semester.getSubjects()):
            i = 0
            while i < len(self.semester.getSubjects()):
                if subject.getID() == self.semester.getSubjects()[i].getID():
                    cl = self.semester.getSubjects()[i].getColor()
                    color.remove_color(cl)
                    self.semester.deleteSubject(self.semester.getSubjects()[i].getID())
                    continue
                i+=1
        else:
            color.remove_color(subject.getColor())
            self.semester.deleteSubject(subject.getID())
            self.removeSel()
        print(self.semester.getSubjects())
        self.loadListSubjectChoiced()
        self.loadListConflict()
        self.loadTable(self.semester.getCurrentSubjects())
        self.enableItemInListFound(subject)

    def addSubject(self, subject: Subject):
        cl = color.hex_code_colors()
        if self.isHaveLecOrLab(subject, self.SUBJECT_FOUND):
            for i in self.isHaveLecOrLab(subject, self.SUBJECT_FOUND):
                self.SUBJECT_FOUND[i].setColor(cl)
                sub = self.SUBJECT_FOUND[i]
                self.semester.addSubject(sub)
        else:
            subject.setColor(cl)
            self.semester.addSubject(subject)
        self.loadListSubjectChoiced()
        self.loadListConflict()
        self.loadTable(self.semester.getCurrentSubjects())
        self.unableItemInListFound()


    # Các phương thức thao tác trên kho dữ liệu
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

    def fillDataToSubjectFound(self, e):
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

    def findSubject(self):
        self.SUBJECT_FOUND.clear()
        self.listView_SubjectDownloaded.clear()
        self.textEdit_thongtin.clear()
        self.textEdit_thongtin.setText('Đang tìm kiếm...')
        subject_name = self.line_findSubject.text()
        file_name = team_config.FOLDER_SAVE_EXCEL+'/'+subject_name+'.xls'

        self.thread_getsubject = ThreadGetSubject(subject_name)
        self.thread_getsubject.signal_foundExcel.connect(self.fillDataToSubjectFound)
        self.thread_getsubject.signal_nonFoundExcel.connect(self.messageError)
        if os.path.exists(file_name):
            self.fillDataToSubjectFound(file_name)
        else:
            self.thread_getsubject.start()


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
        setSubjectChoicedIDs = {i.getID() for i in self.semester.getSubjects()}
        for i in range(self.listView_SubjectDownloaded.count()):
            if self.listView_SubjectDownloaded.item(i).data(Qt.UserRole).getID() in setSubjectChoicedIDs:
                self.listView_SubjectDownloaded.item(i).setHidden(True)

    def enableItemInListFound(self, subject: Subject):
        """Hiển thị Subject đã thêm vào bảng."""
        for i in range(self.listView_SubjectDownloaded.count()):
            if self.listView_SubjectDownloaded.item(i).data(Qt.UserRole).getID() == subject.getID():
                self.listView_SubjectDownloaded.item(i).setHidden(False)


    # Các phương thức kiểm tra và logic
    def isHaveLecOrLab(self, subject: Subject, inList: list) -> List:
        """Kiểm tra List of Subject truyền vào có Môn LEC hay LAB hay không. 
        Nếu có trả về list index của Subject LEC hoặc LAB tương ứng. Nếu không trả về None."""
        output = []
        i = 0
        while i<len(inList):
            if subject.getID() == inList[i].getID():
                output.append(i)
            i+=1
        return output

    def afterSubjectsChanged(self, e):
        """Hàm này chạy bất cứ khi nào bạn thay đổi một Subject vào/ra Semester. 
        Dùng để load lại giao diện cho đúng logic."""
        self.semester.gotoWeek(e)
        self.loadTable(self.semester.getCurrentSubjects())
        self.loadListConflict()


    # Các phương thức phục vụ testing
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
        weekChoicer.choiceWeek.connect(self.afterSubjectsChanged)
        weekChoicer.exec()

    # Các hộp thoại thông báo, được chúng tôi gọi là message
    def messageError(self):
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
        self.f = QDialog()
        uic.loadUi(r'GUI\about_us.ui', self.f)
        self.f.exec()

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())