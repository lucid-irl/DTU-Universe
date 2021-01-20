from re import search

from PyQt5.QtGui import QColor
from class_convertType import ConvertThisQObject
from typing import Dict
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QApplication, QWidget, QPushButton, QLabel


from class_subjectCrawler import *
from class_window import Window
import team_config

class DetailSubjectWindow(Window):

    def __init__(self, subjectData: SubjectData, connectString, minimumButton, maximumButton, closeButton, windowTitle):
        super().__init__(connectString, minimumButton, maximumButton, closeButton, windowTitle)
        self.subjectData = subjectData
        self.jsonData = subjectData.getJson()
        self.subjects = subjectData.getSubjects()
        self.label_subject_code = ConvertThisQObject(self, QLabel, 'subject_code').toQLabel()
        self.label_credit_string = ConvertThisQObject(self, QLabel, 'credit_string').toQLabel()
        self.label_study_unit_type = ConvertThisQObject(self, QLabel, 'study_unit_type').toQLabel()
        self.label_study_type = ConvertThisQObject(self, QLabel, 'study_type').toQLabel()
        self.label_semester = ConvertThisQObject(self, QLabel, 'semester').toQLabel()
        self.label_must_study_subject = ConvertThisQObject(self, QLabel, 'must_study_subject').toQLabel()
        self.label_parallel_subject = ConvertThisQObject(self, QLabel, 'parallel_subject').toQLabel()
        self.tableWidget_detail = ConvertThisQObject(self, QTableWidget, 'tableWidget_detail').toQTableWidget()
        self.renderOverview()
        self.renderDetailTable()

    def renderOverview(self):
        self.windowTitleLabel.setText(self.jsonData['name'])
        self.label_subject_code.setText(self.jsonData['subject_code'])
        self.label_credit_string.setText(self.jsonData['credit_string'])
        self.label_study_unit_type.setText(self.jsonData['study_unit_type'])
        self.label_study_type.setText(self.jsonData['study_type'])
        self.label_semester.setText(self.jsonData['semester'])
        self.label_must_study_subject.setText(self.jsonData['must_study_subject'])
        self.label_parallel_subject.setText(self.jsonData['parallel_subject'])

    def renderDetailTable(self):
        data = self.fromSubjectToListData()
        dataHaveClassGroupName = self.insertClassNameToListData(data)
        numrows = len(dataHaveClassGroupName)
        numcols = len(data[0])
        self.tableWidget_detail.setColumnCount(numcols)
        self.tableWidget_detail.setRowCount(numrows)
        for row in range(numrows):
            # paint class group name
            if len(dataHaveClassGroupName[row])==1:
                item = QTableWidgetItem(dataHaveClassGroupName[row][0])
                item.setBackground(QColor('#e8fcc3'))
                self.tableWidget_detail.setItem(row, 0, item)
                self.tableWidget_detail.setSpan(row, 0, 1, self.tableWidget_detail.columnCount())
            else:
                # add subject
                for column in range(numcols):
                    self.tableWidget_detail.setItem(row, column, QTableWidgetItem((dataHaveClassGroupName[row][column])))
        self.tableWidget_detail.resizeColumnsToContents()
        self.tableWidget_detail.resizeRowsToContents()

    def insertClassNameToListData(self, listSubjecInfo: List[List[str]]) -> List:
        """Chèn class group name vào list data của subject."""
        newData: List = []
        for classGroupName in self.subjectData.getListClassGroupName():
            newData.append([classGroupName])
            for subjectInfoes in listSubjecInfo:
                pattern = '^({})'.format(classGroupName)
                if re.search(pattern, subjectInfoes[0]):
                    newData.append(subjectInfoes)
        return newData

    def filterClassFromJsonData(self)-> Dict[str, Dict[str, Dict]]:
        """Lọc ra những nhóm lớp có trong Json data."""
        pattern = '({})'.format(self.jsonData['subject_code'])
        subjectsJsonList = {key:value for key, value in self.jsonData.items() if re.search(pattern, key)}
        return subjectsJsonList

    def fromSubjectToListData(self) -> List[List]:
        outputData = []
        for subject in self.subjects:
            outputData.append(subject.toListInfo())
        return outputData

if __name__ == "__main__":
    sp = SubjectPage('70','CS','414')
    sd = SubjectData(sp)
    app = QApplication([])

    d = DetailSubjectWindow(sd, team_config.UI_DETAILSUBJECTTABLE, 'button_minimum','button_maximum','button_close','label_windowTitle')
    d.show()
    app.exec()