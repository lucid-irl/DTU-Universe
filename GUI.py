# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from schedule import Schedule, StringToSchedule
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

from getSubject import ThreadGetSubject
from subject import Subject
from customwidget import QCustomQWidget

import xlrd
import os
from PyQt5.QtWidgets import QTableWidgetItem


class Ui_MainWindow(object):

    SUBJECTS_LOAD = []
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(892, 680)
        MainWindow.setMaximumSize(QtCore.QSize(1900, 1200))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_timKiem = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_timKiem.setGeometry(QtCore.QRect(140, 90, 41, 21))
        self.pushButton_timKiem.setObjectName("pushButton_timKiem")
        self.tableWidget_lichHoc = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_lichHoc.setGeometry(QtCore.QRect(200, 80, 531, 311))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget_lichHoc.setFont(font)
        self.tableWidget_lichHoc.setLineWidth(1)
        self.tableWidget_lichHoc.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_lichHoc.setRowCount(19)
        self.tableWidget_lichHoc.setObjectName("tableWidget_lichHoc")
        self.tableWidget_lichHoc.setColumnCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_lichHoc.setHorizontalHeaderItem(6, item)
        self.tableWidget_lichHoc.horizontalHeader().setDefaultSectionSize(70)
        self.tableWidget_lichHoc.verticalHeader().setDefaultSectionSize(15)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(520, 70, 71, 16))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(740, 70, 141, 161))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.listWidget_lopDaChon = QtWidgets.QListWidget(self.groupBox_2)
        self.listWidget_lopDaChon.setGeometry(QtCore.QRect(10, 20, 121, 131))
        self.listWidget_lopDaChon.setObjectName("listWidget_lopDaChon")
        self.lineEdit_tenMon = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_tenMon.setGeometry(QtCore.QRect(20, 90, 111, 20))
        self.lineEdit_tenMon.setObjectName("lineEdit_tenMon")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 81, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 10, 611, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(740, 270, 141, 161))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.listWidget_lopXungDot = QtWidgets.QListWidget(self.groupBox_4)
        self.listWidget_lopXungDot.setGeometry(QtCore.QRect(10, 20, 121, 131))
        self.listWidget_lopXungDot.setObjectName("listWidget_lopXungDot")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 120, 181, 281))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.listWidget_tenLop = QtWidgets.QListWidget(self.groupBox_5)
        self.listWidget_tenLop.setGeometry(QtCore.QRect(10, 20, 161, 201))
        self.listWidget_tenLop.setObjectName("listWidget_tenLop")
        self.pushButton_themLop = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_themLop.setGeometry(QtCore.QRect(40, 230, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_themLop.setFont(font)
        self.pushButton_themLop.setObjectName("pushButton_themLop")
        self.pushButton_xoaLop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_xoaLop.setGeometry(QtCore.QRect(750, 240, 56, 21))
        self.pushButton_xoaLop.setObjectName("pushButton_xoaLop")
        self.pushButton_luuText = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_luuText.setGeometry(QtCore.QRect(820, 240, 56, 21))
        self.pushButton_luuText.setObjectName("pushButton_luuText")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 590, 651, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 410, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.checkBox_giaiDoan1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_giaiDoan1.setGeometry(QtCore.QRect(200, 400, 91, 17))
        self.checkBox_giaiDoan1.setObjectName("checkBox_giaiDoan1")
        self.checkBox_giaiDoan2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_giaiDoan2.setGeometry(QtCore.QRect(300, 400, 91, 17))
        self.checkBox_giaiDoan2.setObjectName("checkBox_giaiDoan2")
        self.plainTextEdit_thongTin = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_thongTin.setGeometry(QtCore.QRect(23, 440, 851, 151))
        self.plainTextEdit_thongTin.setObjectName("plainTextEdit_thongTin")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 892, 21))
        self.menubar.setObjectName("menubar")
        self.menuL_CH_H_C = QtWidgets.QMenu(self.menubar)
        self.menuL_CH_H_C.setObjectName("menuL_CH_H_C")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuL_CH_H_C.addSeparator()
        self.menubar.addAction(self.menuL_CH_H_C.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.addSignal()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_timKiem.setText(_translate("MainWindow", "TÌM"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "7h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "9h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "9h15"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "10h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "10h15"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "11h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "11h15"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "13h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "14h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "15h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "15h15"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "16h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "16h15"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "17h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(14)
        item.setText(_translate("MainWindow", "17h15"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(15)
        item.setText(_translate("MainWindow", "17h45"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(16)
        item.setText(_translate("MainWindow", "18h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(17)
        item.setText(_translate("MainWindow", "19h"))
        item = self.tableWidget_lichHoc.verticalHeaderItem(18)
        item.setText(_translate("MainWindow", "21h"))
        item = self.tableWidget_lichHoc.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Thứ 2"))
        item = self.tableWidget_lichHoc.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Thứ 3"))
        item = self.tableWidget_lichHoc.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Thứ 4"))
        item = self.tableWidget_lichHoc.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Thứ 5"))
        item = self.tableWidget_lichHoc.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Thứ 6"))
        item = self.tableWidget_lichHoc.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Thứ 7"))
        item = self.tableWidget_lichHoc.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Chủ Nhật"))
        self.groupBox_2.setTitle(_translate("MainWindow", "LỚP ĐÃ CHỌN"))
        self.label_3.setText(_translate("MainWindow", "MÔN CẦN TÌM:"))
        self.label.setText(_translate("MainWindow", "PHẦN MỀM MÔ PHỎNG VÀ HỖ TRỢ ĐĂNG KÍ LỊCH HỌC"))
        self.groupBox_4.setTitle(_translate("MainWindow", "LỚP XUNG ĐỘT"))
        self.groupBox_5.setTitle(_translate("MainWindow", "LỚP HIỆN CÓ:"))
        self.pushButton_themLop.setText(_translate("MainWindow", "THÊM >"))
        self.pushButton_xoaLop.setText(_translate("MainWindow", "XÓA"))
        self.pushButton_luuText.setText(_translate("MainWindow", "SAVE TXT"))
        self.label_2.setText(_translate("MainWindow", "by Trần Huy Hoàng - Trần Tuấn Khôi - Nguyễn Nhật Trường"))
        self.label_5.setText(_translate("MainWindow", "Thông tin thêm:"))
        self.checkBox_giaiDoan1.setText(_translate("MainWindow", "GIAI ĐOẠN I"))
        self.checkBox_giaiDoan2.setText(_translate("MainWindow", "GIAI ĐOẠN II"))
        self.menuL_CH_H_C.setTitle(_translate("MainWindow", "LỊCH HỌC"))

    def addSignal(self):
        self.pushButton_timKiem.clicked.connect(self.findSubject)

    def findSubject(self):
        subject_name = self.lineEdit_tenMon.text()
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
            self.SUBJECTS_LOAD.append(subject)
        self.loadListView()

    def loadListView(self):
        for subject in self.SUBJECTS_LOAD:
            self.custom_widget_subject = QCustomQWidget(subject)
            self.myQListWidgetItem = QListWidgetItem(self.listWidget_tenLop)
            self.myQListWidgetItem.setSizeHint(self.custom_widget_subject.sizeHint())
            self.listWidget_tenLop.addItem(self.myQListWidgetItem)
            self.listWidget_tenLop.setItemWidget(self.myQListWidgetItem, self.custom_widget_subject)


    def nonFoundSubject(self):
        QMessageBox.warning(MainWindow, 'Cảnh báo sương sương','Có vẻ như bạn chưa donate, vui lòng donate để sử dụng hết tất cả những tính năng', QMessageBox.Ok)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())