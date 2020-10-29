"""Class này triển khai những chức năng liên quan để việc xếp lịch.
Các chức năng phải được triển khai thành một class, và một phương thức emit() một signal.
Các xử lý logic của các chức năng được triển khai trong semeter."""

from Classes.subject import Subject
from PyQt5.QtCore import pyqtSignal, QThread

from Classes.schedule import *
from Classes.conflict import *
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
        '7:00:00':0,'9:00:00':1,'9:15:00':2,'10:15:00':3,'11:15:00':4,
        '13:00:00':5,'14:00:00':6,'15:00:00':7,'15:15:00':8,'16:15:00':9,'17:15:00':10,'17:45:00':11,'18:45:00':12,'21:00:00':13
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

    def scanSubjectConflict(self) -> List[Conflit]:
        pass

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

