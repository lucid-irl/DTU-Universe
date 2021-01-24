import logging

from PyQt5.QtGui import QColor, QIcon
from class_convertType import ConvertThisQObject
from typing import Dict
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDesktopWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QWidget, QPushButton, QLabel

from class_subjectCrawler import *
from class_window import Window
import team_config


class ButtonAddSubject(QPushButton):

    def __init__(self, subject: Subject):
        super().__init__()
        self.subject = subject

    def getSubject(self) -> Subject:
        return self.subject

class DetailSubjectWindow(Window):
    signal_addSubject = pyqtSignal('PyQt_PyObject')
    ICON_BUTTON_ADD = 'resources/icon_add.svg'
    LIST_BUTTON_ADD_SUBJECT: List[ButtonAddSubject] = []

    def __init__(self, master, subjectData: SubjectData, connectString, minimumButton, maximumButton, closeButton, windowTitle):
        super().__init__(connectString, minimumButton, maximumButton, closeButton, windowTitle)
        self.master = master
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

    def renderOverview(self):
        self.windowTitleLabel.setText(self.jsonData['name'])
        self.setWindowTitle(self.jsonData['name'])
        self.label_subject_code.setText(self.jsonData['subject_code'])
        self.label_credit_string.setText(self.jsonData['credit_string'])
        self.label_study_unit_type.setText(self.jsonData['study_unit_type'])
        self.label_study_type.setText(self.jsonData['study_type'])
        self.label_semester.setText(self.jsonData['semester'])
        self.label_must_study_subject.setText(self.jsonData['must_study_subject'])
        self.label_parallel_subject.setText(self.jsonData['parallel_subject'])

    def renderDetailTable(self):
        data = self.fromSubjectToListData()
        self.dataHaveClassGroupName = self.insertClassNameToListData(data)

        numrows = len(self.dataHaveClassGroupName)
        numcols = len(data[0])+1

        self.tableWidget_detail.setRowCount(numrows)
        self.tableWidget_detail.setColumnCount(numcols)
        diffIndexAddSubjectButton = 0

        for row in range(numrows):
            # paint class group name
            if len(self.dataHaveClassGroupName[row])==1:
                logging.info('row == {}'.format(row))
                item = QTableWidgetItem(self.dataHaveClassGroupName[row][0])
                item.setBackground(QColor('#e8fcc3'))
                self.tableWidget_detail.setItem(row, 0, item)
                self.tableWidget_detail.setSpan(row, 0, 1, self.tableWidget_detail.columnCount())
                diffIndexAddSubjectButton += 1
            else:
                # add subject
                for column in range(numcols):
                    if column == numcols-1:
                        logging.info('row-diffIndexAddSubjectButton {}'.format(row-diffIndexAddSubjectButton))
                        logging.info('len self.subject {}'.format(len(self.subjects)))
                        subject = self.subjects[row-diffIndexAddSubjectButton]
                        
                        button = self.createAddSubjectButton(subject)
                        DetailSubjectWindow.LIST_BUTTON_ADD_SUBJECT.append(button)
                        
                        widget = QWidget()
                        layout = QHBoxLayout()
                        layout.addWidget(button)
                        layout.setAlignment(Qt.AlignCenter)
                        layout.setContentsMargins(0, 0, 0, 0)
                        widget.setLayout(layout)
                        self.tableWidget_detail.setCellWidget(row, column, widget)
                    else:
                        item = QTableWidgetItem(self.dataHaveClassGroupName[row][column])
                        self.tableWidget_detail.setItem(row, column, item)

        self.unableButtonAddSubject()
        self.tableWidget_detail.resizeColumnsToContents()
        self.tableWidget_detail.resizeRowsToContents()

    def show(self):
        """Fit size window for content in table."""
        width = self.sizeHint().width()+50
        height = (QDesktopWidget().size().height()/100)*80
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.hopePointX = centerPoint.x() - width/2
        self.hopePointY = centerPoint.y() - height/2
        self.qrect = QRect(self.hopePointX, self.hopePointY, width, height)
        self.setGeometry(self.qrect)
        super().show()

    def createAddSubjectButton(self, subject: Subject):
        addButton = ButtonAddSubject(subject)
        addButton.setIcon(QIcon(DetailSubjectWindow.ICON_BUTTON_ADD))
        addButton.setToolTip('Thêm môn này vào bảng.')
        addButton.clicked.connect(lambda: self.emitSignalAddSubject(emitter=addButton))
        return addButton

    def unableButtonAddSubject(self):
        currentChoicedSubject = self.master.semester.getSubjects()
        subjectCodes = [subject.getSubjectCode() for subject in currentChoicedSubject]
        for button in DetailSubjectWindow.LIST_BUTTON_ADD_SUBJECT:
            if button.getSubject().getSubjectCode() in subjectCodes:
                button.setEnabled(False)

    def enableButtonAddSubject(self, subject: Subject):
        for button in DetailSubjectWindow.LIST_BUTTON_ADD_SUBJECT:
            if button.getSubject().getSubjectCode() == subject.getSubjectCode():
                button.setEnabled(True)

    def emitSignalAddSubject(self, emitter: ButtonAddSubject):
        self.signal_addSubject.emit(emitter.getSubject())
        self.unableButtonAddSubject()

    def insertClassNameToListData(self, listSubjecInfo: List[List[str]]) -> List:
        """Chèn class group name vào list data của subject."""
        newData: List = []
        for classGroupName in self.subjectData.getListClassGroupName():
            newData.append([classGroupName])
            for subjectInfoes in listSubjecInfo:
                pattern = '({})[0-9]*$'.format(classGroupName)
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
    d.signal_addSubject.connect(lambda s: print(s))
    d.show()
    app.exec()