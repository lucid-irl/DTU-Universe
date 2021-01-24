from class_dialogNotification import NotificationWindow
import logging
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from class_convertType import ConvertThisQObject
from class_subjectCrawler import SubjectData, SubjectPage
from team_config import UI_SAVE_EXCEL
from typing import Dict, List
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from class_window import Window
from class_semester import Semester
from class_schedule import WEEK
from class_subject import Subject, getTotalCredit, indexOfLecLab, isHaveLecLab, mergeListSubject, mergeTwoSubject, reduceSubject
import cs4rsa_helpfulFunctions
import xlsxwriter


class SaveExcel(Window):
    def __init__(self, connectString, minimumButton, maximumButton, closeButton, windowTitle, subjects: List[Subject]):
        super().__init__(connectString, minimumButton, maximumButton, closeButton, windowTitle)
        self.lineEdit_fileName = ConvertThisQObject(self, QLineEdit, 'lineEdit_fileName').toQLineEdit()
        self.button_ok = ConvertThisQObject(self, QPushButton, 'button_ok').toQPushButton()
        self.button_ok.clicked.connect(self.beforeRun)
        self.subjects = subjects

    def beforeRun(self):
        if self.lineEdit_fileName.text().strip() == '':
            NotificationWindow('Thông báo','Có vẻ như bạn chưa nhập tên file kìa','À mình quên mất').exec()
        else:
            try:
                self.run()
            except:
                NotificationWindow('Thông báo', 'Có vẻ như bạn đang mở file có tên bạn vừa nhập, hãy tắt file đó đi và thử lại','Ok nhé')

    def run(self):
        workbook = xlsxwriter.Workbook(self.lineEdit_fileName.text()+'.xlsx')
        worksheet = workbook.add_worksheet()

        # write data
        self.subjects = reduceSubject(self.subjects)
        array = self.getListSubjectInfo(self.subjects)

        # write header
        removes = ['places','name','empty_seat', 'study_hours','rooms','study_week','registration_term','registration_status','implementation_status']
        headers = list(SaveExcel.getHeader(removes).values())
        col = 0
        worksheet.write_row(0, 0, headers)

        # write data
        startDataRow = 1
        for index, dataRow in enumerate(array, 0):
            dataRow = SaveExcel.removeItemFromListKey(dataRow, removes)
            worksheet.write_row(index+startDataRow, col, list(dataRow.values()))

        # write color
        colors = SaveExcel.getColors(self.subjects)
        indexOfSubjectCode = cs4rsa_helpfulFunctions.getIndexOfKeyInDict(SaveExcel.getHeader(removes), 'subject_code')
        array = [list(value.values()) for value in array]
        colData = cs4rsa_helpfulFunctions.getColFromMatrix(array, indexOfSubjectCode)
        for i in range(len(colData)):
            cell_format = workbook.add_format({'bg_color':colors[i]})
            worksheet.write(i+startDataRow, indexOfSubjectCode, colData[i], cell_format)
        
        # total credit
        totalCredit = getTotalCredit(self.subjects)
        indexCreditCell = list(SaveExcel.getHeader(removes).keys()).index('credit')
        row = len(array)+1
        col = indexCreditCell-1
        worksheet.write_row(row, col, ['Tổng số tín chỉ', totalCredit])

        # write table
        col=0
        row=row+2
        subjectPhase1 = Semester.filterPhase_New(self.subjects, 1)
        subjectPhase2 = Semester.filterPhase_New(self.subjects, 2)
        SaveExcel.paintTable(row, col, subjectPhase1, 1, worksheet, workbook)
        SaveExcel.paintTable(row, 9, subjectPhase2, 2, worksheet, workbook)
        workbook.close()
        NotificationWindow('Thông báo','Xuất thành công','Cảm ơn rất nhiều').exec()

    @staticmethod
    def paintTable(row, col, subjects: List[Subject], phase: int, worksheet: Worksheet, workbook: Workbook):
        worksheet.write(row, col, 'Giai đoạn {}'.format(phase))

        # paint date
        rowDate = row + 1
        colDate = col + 1
        worksheet.write_row(rowDate, colDate, WEEK)

        # paint timechain
        timeChain = list(Semester.TIME_CHAINS.keys())
        rowTimeChain = row + 2
        colTimeChain = col
        worksheet.write_column(rowTimeChain, colTimeChain, timeChain)
        # paint table
        colStartTable = col+1
        rowStartTable = row+2

        for subject in subjects:
            color = subject.getColor()
            format = workbook.add_format({'bg_color':color})
            days = subject.getSchedule().getDatesOfLesson()
            for day in days:
                start_time_subjects = subject.getSchedule().getStartTimeOfDate(day)
                end_time_subjects = subject.getSchedule().getEndTimeOfDate(day)
                for i in range(len(start_time_subjects)):
                    start = str(start_time_subjects[i])
                    end = str(end_time_subjects[i])
                    start_row = Semester.getTimeChains()[start] + rowStartTable
                    end_row = Semester.getTimeChains()[end] + rowStartTable
                    column = WEEK.index(day)+colStartTable
                    for row in range(start_row, end_row+1):
                        worksheet.write(row, column, subject.getSubjectCode(), format)

    @staticmethod
    def removeItemFromListKey(data: Dict, listKey: List[str]):
        for key in listKey:
            data.pop(key)
        return data

    @staticmethod
    def getHeader(listKey: List[str]) -> Dict:
        headers = {
        'register_code': 'Mã đăng ký', 
        'subject_code': 'Mã môn',
        'name': 'Tên môn',
        'empty_seat': 'Còn trống',
        'credit':'Số tín chỉ', 
        'type':'Loại hình', 
        'study_hours':'Giờ học',
        'teachers':'Giảng viên', 
        'places':'Nơi học', 
        'rooms':'Phòng học',
        'study_week':'Tuần học', 
        'registration_term':'Hạn đăng ký', 
        'registration_status':'Tình trạng đăng ký', 
        'implementation_status':'Tình trạng triển khai'}
        return SaveExcel.removeItemFromListKey(headers, listKey)

    @staticmethod
    def getListSubjectInfo(subjects: List[Subject]):
        output = []
        logging.info('getListSubjectInfo {}'.format(subjects))
        for subject in subjects:
            output.append(subject.toDictInfoRenderExcel())
        return output

    def reduceSubject(self):
        """Gộp những lớp LEC/LAB lại với nhau và trả về một list Subject mới."""
        newSubjects: List[Subject] = []
        i = 0
        while len(self.subjects) > 0 and isHaveLecLab(self.subjects):
                indexs = indexOfLecLab(self.subjects[i], self.subjects)
                listSubjectLecLab: List[Subject] = cs4rsa_helpfulFunctions.getListObjectFromIndex(indexs, self.subjects)
                mergedSubject = mergeListSubject(listSubjectLecLab)
                newSubjects.append(mergedSubject)
                self.subjects = cs4rsa_helpfulFunctions.getNewListWithoutIndex(indexs, self.subjects)
        return newSubjects + self.subjects

    @staticmethod
    def getColors(subjects: List[Subject]):
        return [subject.getColor() for subject in subjects]

if __name__ == "__main__":
    app = QApplication([])
    sp = SubjectPage('71','CS','414')
    sd = SubjectData(sp)
    d = SaveExcel(UI_SAVE_EXCEL, 'button_minimum','button_maximum', 'button_close','label_windowTitle',sd.getSubjects())
    d.show()
    app.exec()