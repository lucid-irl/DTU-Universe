from subject import Subject
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from schedule import *


class Semeter:

    def __init__(self, table: QTableWidget) -> None:
        self.table = table
        self.subject = []

    def addSubjectToSemeter(self, subject: Subject):
        self.SUBJECTS.append(subject)

    def LoadTable(self):
        # subject1 = Subject()
        for subject1 in self.SUBJECTS:
            days = subject1.getSchedule().getDatesOfLesson()
            for day in days:
                start_time_subjects = subject1.getSchedule().getStartTimeOfDate(day)
                end_time_subjects = subject1.getSchedule().getEndTimeOfDate(day)
                for i in range(len(start_time_subjects)):
                    start = start_time_subjects[i]
                    end = end_time_subjects[i]
                    column = WEEK.index(day)
                    for pen in range(start, end+1):
                        self.table.setItem(pen, column, QTableWidgetItem())
                        self.table.item(pen, column).setBackground(QColor(100,100,150))