from re import sub
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic

from class_customwidget import QCustomQWidget
from class_semeter import *
from class_subject import Subject
from class_schedule import StringToSchedule

from thread_getSubject import ThreadGetSubject

import sys
import os
import xlrd
import color
import team_config

class Main(QMainWindow):
    """Class này chỉ đảm nhiệm việc xử lý giao diện."""

    SUBJECT_FOUND = []

    def __init__(self):
        super(Main, self).__init__()

        uic.loadUi(team_config.FOLDER_UI+'/'+team_config.USE_UI, self)

        self.button_findSubject = self.findChild(QPushButton,'pushButton_timKiem')
        self.button_addSujectToTable = self.findChild(QPushButton, 'pushButton_themLop')
        self.button_updateSubject = self.findChild(QPushButton, 'pushButton_themLop_2')
        self.button_deleleSubjectFromTable = self.findChild(QPushButton, 'pushButton_xoaLop')
        self.button_saveExcel = self.findChild(QPushButton, 'pushButton_luuText')

        self.listView_SubjectDownloaded = self.findChild(QListWidget, 'listWidget_tenLop')
        self.listView_SubjectChoiced = self.findChild(QListWidget, 'listWidget_lopDaChon')
        self.listView_SubjectConflict = self.findChild(QListWidget, 'listWidget_lopXungDot')

        self.line_findSubject = self.findChild(QLineEdit, 'lineEdit_tenMon')

        self.checkBox_phase1 = self.findChild(QCheckBox, 'checkBox_giaiDoan1')
        self.checkBox_phase2 = self.findChild(QCheckBox, 'checkBox_giaiDoan2')

        self.textEdit_thongtin = self.findChild(QTextEdit, 'textEdit_thongtin')
        self.textEdit_thongke = self.findChild(QTextEdit, 'textEdit_thongke')

        self.table_Semeter = self.findChild(QTableWidget, 'tableWidget_lichHoc')

################## hot fix ##################################
        # self.button_findSubject = QPushButton()
        # self.button_addSujectToTable = QPushButton()
        # self.button_updateSubject = QPushButton()
        # self.button_deleleSubjectFromTable = QPushButton()
        # self.button_saveExcel = QPushButton()

        # self.listView_SubjectDownloaded = QListWidget()
        # self.listView_SubjectChoiced = QListWidget()
        # self.listView_SubjectConflict = QListWidget()

        # self.line_findSubject = QLineEdit()

        # self.checkBox_phase1 = QCheckBox()
        # self.checkBox_phase2 = QCheckBox()

        # self.textEdit_thongtin = QTextEdit()

        # self.table_Semeter = QTableWidget()
################## hot fix ##################################

        self.semeter = Semeter()
        self.show()   
        self.addSignalWidget()


    def addSignalWidget(self):
        self.button_findSubject.clicked.connect(self.findSubject)
        self.button_addSujectToTable.clicked.connect(self.addSubjectToTable)
        self.button_deleleSubjectFromTable.clicked.connect(self.deleteSubject)
        self.listView_SubjectDownloaded.itemClicked.connect(self.showInfoSubject)
        self.listView_SubjectChoiced.itemClicked.connect(self.showInfoSubject)


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
                        self.table_Semeter.setItem(pen, column, QTableWidgetItem())
                        self.table_Semeter.item(pen, column).setBackground(color)


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


    def addSubjectToTable(self):
        item = self.listView_SubjectDownloaded.currentItem()
        if item:
            subject = item.data(Qt.UserRole)
            subject.setColor(color.getColor())
            self.semeter.addSubjectToSemeter(subject)
            self.loadListChoosed()
            self.loadTable(self.semeter.getSubjectsInSemeter())
            self.scanConflict()
        else:
            QMessageBox.warning(self,
                'Một thông báo sương sương',
                """Vui lòng chọn một môn nào đó để thêm vào lịch. Bạn có thể Donate để mở khoá tính năng thêm một lúc nhiều môn.""",
                QMessageBox.Ok)


<<<<<<< HEAD
    def scanConflict(self):git 
=======
    def scanConflict(self) -> List[str]:
>>>>>>> 3e62061c2f9a243521707549b9052bcf638b84bf
        if len(self.semeter.getSubjectsInSemeter()) >= 2:
            output = []
            conflits = self.semeter.scanSubjectConflict()
            for conflict in conflits:
                output.append(conflict.getConflitTime())
            return output


    def findSubject(self):
        self.SUBJECT_FOUND.clear()
        self.listView_SubjectDownloaded.clear()
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
            subject = Subject(id, name, seats, credit, schedule, teacher, place, week_range, status)
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
            self.custom_widget_subject = QCustomQWidget(subject)

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


    def nonFoundSubject(self):
        QMessageBox.warning(self, 'Cảnh báo sương sương','Có vẻ như bạn chưa donate, vui lòng donate để sử dụng hết tất cả những tính năng', QMessageBox.Ok)

    

app = QApplication(sys.argv)
window = Main()
sys.exit(app.exec_())