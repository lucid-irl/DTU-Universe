from subject import Subject
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from schedule import *
from color import *
import random


class Semeter:

    time_chain = {'7:00:00':0,'9:00:00':1,'9:15:00':2,'10:15:00':4,'11:15:00':5,'13:00:00':7,'14:00:00':8,'15:00:00':9,'16:00:00':11,'16:15:00':12,'17:00:00':13,'17:45:00':14,'19:00:00':15,'21:00:00':16}
    color_choices = []

    def __init__(self, table: QTableWidget) -> None:
        self.table = table
        self.subject = []

    def getSubject(self):
        return self.subject

    def addSubjectToSemeter(self, subject: Subject):
        self.subject.append(subject)
        self.LoadTable()

    def deleteSubject(self, name):
        for j in range(len(self.subject)):
            if self.subject[j].getName() == name:
                self.subject.pop(j)
        print(self.subject)
        self.LoadTable()
        self.removeAllItemTable()

    def removeAllItemTable(self):
        for i in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                self.table.setItem(i, c, QTableWidgetItem())
                self.table.item(i, c).setBackground(QColor(255,255,255))

    def LoadTable(self):
        for subject1 in self.subject:
            days = subject1.getSchedule().getDatesOfLesson()
            cl = random.choice(list_color)
            self.color_choices.append(cl)
            mau = QColor(cl)
            for day in days:
                start_time_subjects = subject1.getSchedule().getStartTimeOfDate(day)
                end_time_subjects = subject1.getSchedule().getEndTimeOfDate(day)
                for i in range(len(start_time_subjects)):
                    start = str(start_time_subjects[i])
                    end = str(end_time_subjects[i])
                    start_row = self.time_chain[start]
                    end_row = self.time_chain[end]
                    print('start row:', start_row)
                    print('end row:', end_row)
                    print('column:', WEEK.index(day))
                    column = WEEK.index(day)
                    for pen in range(start_row, end_row+1+1):
                        self.table.setItem(pen, column, QTableWidgetItem())
                        self.table.item(pen, column).setBackground(mau)