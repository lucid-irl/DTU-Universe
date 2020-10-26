from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from customwidget import QCustomQWidget

from semeter import Semeter
from subject import Subject
from schedule import Schedule, StringToSchedule

from thread_getSubject import ThreadGetSubject

import sys
import os
import xlrd, xlwt

class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        self.subject_found = []

        uic.loadUi('GUI/GUI.ui', self)

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

        self.plainText = self.findChild(QTextEdit, 'plainTextEdit_thongTin')

        self.table_Semeter = self.findChild(QTableWidget, 'tableWidget_lichHoc')

################## hot fix ##################################
        self.button_findSubject = QPushButton()
        self.button_addSujectToTable = QPushButton()
        self.button_updateSubject = QPushButton()
        self.button_deleleSubjectFromTable = QPushButton()
        self.button_saveExcel = QPushButton()

        self.listView_SubjectDownloaded = QListWidget()
        self.listView_SubjectChoiced = QListWidget()
        self.listView_SubjectConflict = QListWidget()

        self.line_findSubject = QLineEdit()

        self.checkBox_phase1 = QCheckBox()
        self.checkBox_phase2 = QCheckBox()

        self.plainText = QPlainTextEdit()

        self.table_Semeter = QTableWidget()
################## hot fix ##################################


        self.semeter = Semeter(self.table_Semeter)

        self.show()
        self.addSignal()

    def addSignal(self):
        self.button_findSubject.clicked.connect(self.findSubject)
        self.button_addSujectToTable.clicked.connect(self.addSubjectToTable)
        self.button_deleleSubjectFromTable.clicked.connect(self.deleteSubject)

    def loadListChoosed(self):
        for subject in self.semeter.getSubject():
            self.custom_widget_subject = QCustomQWidget(subject)
            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectChoiced)

            self.myQListWidgetItem.setData(Qt.UserRole, subject)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())

            self.listView_SubjectChoiced.addItem(self.myQListWidgetItem)
            self.listView_SubjectChoiced.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)

    def deleteSubject(self):
        subject = self.listView_SubjectChoiced.currentItem().data(Qt.UserRole)
        self.semeter.deleteSubject(subject.getName())
        self.listView_SubjectChoiced.clear()
        self.loadListChoosed()

    def addSubjectToTable(self):
        subject = self.listView_SubjectDownloaded.currentItem().data(Qt.UserRole)
        self.semeter.addSubjectToSemeter(subject)
        self.loadListChoosed()

    def findSubject(self):
        self.subject_found.clear()
        self.listView_SubjectDownloaded.clear()
        subject_name = self.line_findSubject.text()
        file_name = subject_name+'.xls'
        self.thread_getsubject = ThreadGetSubject(subject_name)
        self.thread_getsubject.foundExcel.connect(self.fillDataToSubjectTempList)
        self.thread_getsubject.nonFoundExcel.connect(self.nonFoundSubject)
        if os.path.exists(file_name):
            self.fillDataToSubjectTempList(file_name)
        else:
            self.thread_getsubject.start()

    def fillDataToSubjectTempList(self, e):
        wb = xlrd.open_workbook(e)
        sheet = wb.sheet_by_index(0)
        
        for i in range(1, sheet.nrows):
            id = sheet.cell_value(i, 1)
            name = sheet.cell_value(i, 2)
            seats = sheet.cell_value(i, 1)
            credit = int(sheet.cell_value(i, 6))
            schedule = StringToSchedule(sheet.cell_value(i, 3))
            teacher = sheet.cell_value(i, 5)
            place = sheet.cell_value(i, 4)
            week_range = sheet.cell_value(i, 8).split('--')
            status =  int(sheet.cell_value(i, 9))
            subject = Subject(id, name, seats, credit, schedule, teacher, place, week_range, status)
            self.subject_found.append(subject)
        self.loadListView()

    def loadListView(self):
        for subject in self.subject_found:
            self.custom_widget_subject = QCustomQWidget(subject)
            self.myQListWidgetItem = QListWidgetItem(self.listView_SubjectDownloaded)
            self.myQListWidgetItem.setData(Qt.UserRole, subject)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())
            self.listView_SubjectDownloaded.addItem(self.myQListWidgetItem)
            self.listView_SubjectDownloaded.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)


    def nonFoundSubject(self):
        QMessageBox.warning(self, 'Cảnh báo sương sương','Có vẻ như bạn chưa donate, vui lòng donate để sử dụng hết tất cả những tính năng', QMessageBox.Ok)

    

app = QApplication(sys.argv)
window = Main()
sys.exit(app.exec_())