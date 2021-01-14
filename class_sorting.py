from team_config import *
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QListWidget, QApplication, QDialog
from PyQt5 import uic
from class_convertType import ConvertThisQObject

import sys

import json

class FillMajorData:
    def __init__(self, file):
        self.file = file
        with open(file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def getListMajor(self) -> list:
        listMajor = []
        for dict in self.data:
            major = dict['major']
            listMajor.append(major)
        return listMajor

    def getListSemesterInfo(self, index) -> list:
        major = self.data[index]
        semesterInfo = major['semester_info']
        listSemesterInfo = []
        for semester in semesterInfo:
            name = semester['semester']
            listSemesterInfo.append(name)
        return listSemesterInfo

    def getSubject(self, indexMajor, indexSemester) -> list:
        major = self.data[indexMajor]
        listSubject = major['semester_info'][indexSemester]['subjects']
        listSubjectInfo = []
        for subject in listSubject:
            subjectInfo = subject['id'] +': '+ subject['name']
            listSubjectInfo.append(subjectInfo)
        return listSubjectInfo

class PredictSubject(QDialog):
    def __init__(self, jsonPath) -> None:
        super(QWidget, self).__init__()
        self.jsonPath = jsonPath
        self.filldata = FillMajorData(jsonPath)
        uic.loadUi("guis/predict_subject.ui", self)
        #uic.loadUi(team_config.FOLDER_UI+"/"+team_config.PREDICT_SUBJECT, self)
        self.button_find = ConvertThisQObject(self, QPushButton,'pushButtonFind').toQPushButton()
        self.button_sort = ConvertThisQObject(self, QPushButton,'pushButtonSort').toQPushButton()
        self.comboBox_major = ConvertThisQObject(self, QComboBox, 'comboBoxMajor').toQComboBox()
        self.comboBox_semester = ConvertThisQObject(self, QComboBox, 'comboBoxSemester').toQComboBox()
        self.listWidget_listSubject = ConvertThisQObject(self, QListWidget, 'listWidget_listSubject').toQListWidget()
        self.connectSignal()
        self.fillDataToMajorComboBox()

    def connectSignal(self):
        self.button_find.clicked.connect(self.fillSubjectToListWidget)
        self.comboBox_major.currentIndexChanged.connect(self.fillDataToSemesterCombobox)

    def fillDataToMajorComboBox(self):
        print('major',self.comboBox_major.currentIndex)
        data = self.filldata.getListMajor()
        self.comboBox_major.addItems(data)

    def fillDataToSemesterCombobox(self, index):
        print('major',index, 'semester',self.comboBox_semester.currentIndex)
        self.comboBox_semester.clear()
        data = self.filldata.getListSemesterInfo(index)
        self.comboBox_semester.addItems(data)
    
    def fillSubjectToListWidget(self):
        self.listWidget_listSubject.clear()
        indexMajor = self.comboBox_major.currentIndex()
        indexSemester = self.comboBox_semester.currentIndex()
        data = self.filldata.getSubject(indexMajor, indexSemester)
        self.listWidget_listSubject.addItems(data)


'''class AutoSortingClass:
    def __init__(self, file):
        self.file = file
        with open(file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def getListMajor(self) -> list:
        listMajor = []
        for dict in self.data:
            major = dict['major']
            listMajor.append(major)

        print(listMajor)
        return listMajor

    def getListSemesterInfo(self, index) -> list:
        major = self.data[index]
        semesterInfo = major['semester_info']
        listSemesterInfo = []
        for semester in semesterInfo:
            name = semester['semester']
            listSemesterInfo.append(name)
        print(listSemesterInfo)
        return listSemesterInfo

    def getSubjectID(self, indexMajor, indexSemester) -> list:
        major = self.data[indexMajor]
        listSubject = major['semester_info'][indexSemester]['subjects']
        listSubjectID = []
        for subject in listSubject:
            listSubjectID.append(subject['id'])
        print(listSubjectID)
        return listSubjectID
'''

app = QApplication(sys.argv)
window = PredictSubject('semester_info.json')
window.show()
sys.exit(app.exec_())

