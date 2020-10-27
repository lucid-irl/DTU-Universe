from Classes.subject import Subject
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from Classes.schedule import *
from color import *
import random


class Semeter:
    """
    Class này là class trung gian giữa Subject và Table
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Class này chịu trách nhiệm hiển thị trực quan lịch của một Subject lên Table. Các thao tác liên quan đến Table
    có trên giao diện đều phải thông qua class này và các phương thức của nó.
    """

    TIME_CHAINS = {'7:00:00':0,'9:00:00':1,'9:15:00':2,'10:15:00':3,'11:15:00':4,'13:00:00':5,'14:00:00':6,'15:00:00':7,'15:15:00':8,'16:15:00':9,'17:15:00':10,'17:45:00':11,'18:45:00':12,'21:00:00':13}
    color_choices = []

    def __init__(self, table: QTableWidget) -> None:
        self.table = table
        self.subjects = []

    def getSubject(self):
        return self.subjectss

    def addSubjectToSemeter(self, subject: Subject):
        self.subjects.append(subject)
        self.loadTable()

    def deleteSubject(self, name):
        for j in range(len(self.subjects)):
            if self.subjects[j].getName() == name:
                self.subjects.pop(j)
        self.loadTable()

    def resetTableColor(self):
        """Xoá hết màu có trên Table."""
        for i in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                self.table.setItem(i, c, QTableWidgetItem())
                self.table.item(i, c).setBackground(QColor(255,255,255))

    def loadTable(self):
        """Quét lại bộ chứa subject và hiển thị lên Table."""
        self.resetTableColor()
        for subject1 in self.subjects:
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
                    start_row = self.TIME_CHAINS[start]
                    end_row = self.TIME_CHAINS[end]
                    column = WEEK.index(day)
                    for pen in range(start_row, end_row+1+1):
                        self.table.setItem(pen, column, QTableWidgetItem())
                        self.table.item(pen, column).setBackground(mau)