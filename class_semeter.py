"""Class này triển khai những chức năng liên quan để việc xếp lịch.
Các chức năng phải được triển khai thành một class, và một phương thức emit() một signal.
Các xử lý logic của các chức năng được triển khai trong semeter."""

from PyQt5.QtCore import pyqtSignal, QThread
from class_subject import Subject
from class_schedule import *
from class_conflict import *
from color import *


class Semeter:
    """
    Class này là class trung gian giữa Subject và Table
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Class này chịu trách nhiệm hiển thị trực quan lịch của một Subject lên Table. Các thao tác liên quan đến Table
    có trên giao diện đều phải thông qua class này và các phương thức của nó.
    
    Trong Class này triển khai các xử lý logic và trả về cho giao diện.
    Nhiệm vụ của giao diện là bắt signal và cập nhật UI.
    """

    TIME_CHAINS = {
        '7:00:00':0,
        '9:00:00':1,
        '9:15:00':2,
        '10:15:00':3,
        '11:15:00':4,
        '13:00:00':5,
        '13:15:00':6,
        '14:00:00':7,
        '15:00:00':8,
        '15:15:00':9,
        '15:45:00':10,
        '16:15:00':11,
        '17:00:00':12,
        '17:15:00':13,
        '17:45:00':14,
        '18:45:00':15,
        '19:15:00':16,
        '21:00:00':17
        }

    DATE_CHAINS = {
        Monday: 0,
        Tuseday: 1,
        Wednesday: 2,
        Thursday: 3,
        Friday: 4,
        Saturday: 5,
        Sunday: 6,
    }
    
    SUBJECTS = []

    def getSubjectsInSemeter(self) -> List[Subject]:
        return self.SUBJECTS
    
    def getTimeChains(self):
        return self.TIME_CHAINS

    def addSubjectToSemeter(self, subject: Subject):
        self.SUBJECTS.append(subject)

    def deleteSubject(self, name):
        for j in range(len(self.SUBJECTS)):
            if self.SUBJECTS[j].getName() == name:
                self.SUBJECTS.pop(j)
                break

    def scanSubjectConflict(self) -> List[List[Dict[str,Tuple[str]]]]:
        """Bắt cặp tất cả Subject có trong danh sách trả về List chứa Conflicts.

        [[{'T6': ('9:15:00', '10:15:00')}, {'T6': ('7:00:00', '9:00:00')}, {'T6': ('7:00:00', '10:15:00')}]]"""
        conflicts = []
        output = []
        tempSubjectsList = self.SUBJECTS.copy()
        while len(tempSubjectsList) > 1:
            baseSubject = tempSubjectsList[0]
            for i in range(1,len(tempSubjectsList)):
                if i==len(tempSubjectsList):
                    break
                conflict = Conflit(baseSubject, tempSubjectsList[i])
                if conflict.isConflict():
                    conflicts.append(conflict)
            tempSubjectsList.pop(0)
        for conflict in conflicts:
            output.append(conflict.getConflitTime())
        return output


    def resetTableColor(self):
        """Xoá hết màu có trên Table."""
        self.signal_resetTable(self.SUBJECTS)


class AddSubject(QThread):
    signal_loadTable = pyqtSignal('PyQt_PyObject')

    def __init__(self, subject: Subject, semeter: Semeter) -> None:
        super(QThread, self).__init__()
        self.semeter = semeter
        self.subject = subject

    def run(self):
        self.semeter.addSubjectToSemeter(self.subject)
        self.signal_loadTable.emit(self.semeter.getSubjectInSemeter())

class DeleteSubject(QThread):
        
    signal_loadTable = pyqtSignal('PyQt_PyObject')

    def __init__(self, name: str, semeter: Semeter) -> None:
        super(QThread, self).__init__()
        self.semeter = semeter
        self.name = name

    def run(self):
        self.semeter.deleteSubject(self.name)
        self.signal_loadTable.emit(self.semeter.getSubjectInSemeter())

class ScanConflictSubject:
        
    signal_loadTable = pyqtSignal('PyQt_PyObject')

    def __init__(self, semeter: Semeter) -> None:
        self.semeter = semeter

    def run(self):
        conflicts = self.semeter.scanSubjectConflict()
        self.signal_loadTable.emit(conflicts)

