from PyQt5.QtCore import QObject, pyqtSignal

from class_subject import Subject
from class_schedule import *
from class_conflict import *
from cs4rsa_color import *

import logging

# logging.basicConfig(level=logging.INFO)

class Semester(QObject):
    """
    Class này là class trung gian giữa Subject và Table
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Bao gồm tìm lịch, thêm lịch và xử lý xung đột.
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
    
    # subject mà người dùng chọn sẽ nằm ở đây
    SUBJECTS: List[Subject] = []
    CONFLICT = []
    # list of week do initSemester sẽ nằm ở đây
    SEMESTER = []
    SEMESTER_INDEX = 0

    # signal
    signal_indexChanged = pyqtSignal('PyQt_PyObject')
    signal_addSubject = pyqtSignal('PyQt_PyObject')
    signal_deleteSubject = pyqtSignal('PyQt_PyObject')


    # IMPORTANT!!!
    def addSubject(self, subject: Subject):
        """Thêm một Subject vào Semester."""
        logging.info('addSubject run')
        Semester.SUBJECTS.append(subject)
        self.initSemester()
        self.setSemesterIndex(0)
        self.signal_addSubject.emit(subject)

    def deleteSubject(self, subject: Subject):
        """Xoá một Subject khỏi Semester dựa theo ID."""
        logging.info('deleteSubject run --> {0}'.format(subject))
        for i in range(len(Semester.SUBJECTS)):
            logging.info('in deleteSubject --> i = {0}'.format(i))
            if Semester.SUBJECTS[i].getSubjectCode() == subject.getSubjectCode():
                sb = Semester.SUBJECTS.pop(i)
                logging.info('DELETED --> {0}'.format(sb))
                break
        self.initSemester()
        self.setSemesterIndex(0)
        self.signal_deleteSubject.emit(subject)

    # IMPORTANT!!!
    def initSemester(self) -> List[List[Subject]]:
        """
        Khởi tạo lại danh sách tuần học mỗi lần Thêm, Xoá.
        """
        logging.info('initSemester run')
        Semester.SEMESTER: List[List[Subject]] = [[] for i in range(self.getMaxWeekInSemester())]
        for subject in Semester.SUBJECTS:
            for i in range(subject.getWeekStart()-1, subject.getWeekEnd()):
                Semester.SEMESTER[i].append(subject)

    def getSubjects(self) -> List[Subject]:
        """Trả về danh sách tất cả các Subject có trong một học kỳ."""
        logging.info('getSubjects run')
        return Semester.SUBJECTS
    
    def getCurrentSubjects(self) -> List[Subject]:
        """Trả về danh sách các Subject có trong tuần hiện tại."""
        logging.info('getCurrentSubjects run')
        if len(Semester.SEMESTER):
            return Semester.SEMESTER[Semester.SEMESTER_INDEX]
        else:
            return []
        
    def getWeek(self, week):
        """Phương thức này trả về một list các Subject trong một Tuần cụ thể của Semester. Nếu tuần đó không tồn tại
        phương thức này trả về một list rỗng."""
        logging.info('getWeek run')
        if week < 0 or week >= Semester.SEMESTER_INDEX:
            return []
        else:
            return Semester.SEMESTER[week]

    # Các thao tác trên Semester
    @staticmethod
    def getCurrentSemesterIndex():
        """Trả về index hiện tại của Semester, tương ứng với tuần thứ `index+1`."""
        return Semester.SEMESTER_INDEX

    @staticmethod
    def getTimeChains():
        return Semester.TIME_CHAINS
    
    def getMaxWeekInSemester(self) -> int:
        """Trả về số Tuần kéo dài tối đa mà Semester có thể có."""
        logging.info('getMaxWeekInSemester run')
        max = 0
        for subject in Semester.SUBJECTS:
            if subject.getWeekEnd() > max:
                max = subject.getWeekEnd()
        return max

    def pairingSubjectInWeek(self) -> List[Tuple[Subject]]:
        """Bắt cặp các Subject có trong danh sách Subject được thêm vào Semester."""
        logging.info('pairingSubjectInWeek run')
        pairedSubjects = []
        tempSubjects = Semester.SUBJECTS.copy()
        while len(tempSubjects) != 1:
            baseSubject = tempSubjects[0]
            for i in range(1,len(tempSubjects)):
                if i==len(tempSubjects):
                    break
                pairedSubjects.append((baseSubject, tempSubjects[i]))
            tempSubjects.pop(0)
        return pairedSubjects

    def getConflicts(self) -> List[Conflict]:
        """Trả về list conflict của tuần hiện tại."""
        logging.info('getConflicts run')
        if len(Semester.SUBJECTS) < 2:
            return []
        conflictsOutput = []
        pairedSubjects: List[Tuple[Subject]] = self.pairingSubjectInWeek()
        for pairedSubject in pairedSubjects:
            conflict = Conflict(pairedSubject[0], pairedSubject[1])
            if conflict.getConflictTime():
                conflictsOutput.append(conflict)
        return conflictsOutput

    def setSemesterIndex(self, index: int):
        logging.info('setSemesterIndex run')
        Semester.SEMESTER_INDEX = index
        self.signal_indexChanged.emit(Semester.SEMESTER_INDEX)

    # Điều khiển Week Context của Semester
    def nextWeek(self):
        """Phương thức này sẽ tăng index của Semester lên 1. Thao tác trên biến SEMESTER_INDEX."""
        logging.info('nextWeek run')
        if Semester.SEMESTER_INDEX >= 0 and Semester.SEMESTER_INDEX+1 < len(Semester.SEMESTER):
            if Semester.SEMESTER_INDEX < self.getMaxWeekInSemester():
                Semester.SEMESTER_INDEX+=1
                self.signal_indexChanged.emit(Semester.SEMESTER_INDEX)

    def previousWeek(self):
        """Phương thức này sẽ giảm index của Semester xuống 1. Thao tác trên biến SEMESTER_INDEX."""
        logging.info('previousWeek run')
        if Semester.SEMESTER_INDEX-1 >= 0 and Semester.SEMESTER_INDEX < len(Semester.SEMESTER):
            if Semester.SEMESTER_INDEX > 0:
                Semester.SEMESTER_INDEX-=1
                self.signal_indexChanged.emit(Semester.SEMESTER_INDEX)

    def gotoWeek(self, week: int) -> bool:
        logging.info('gotoWeek run')
        if len(Semester.SEMESTER) > 0:
            if Semester.SEMESTER_INDEX >= 0 and Semester.SEMESTER_INDEX < len(Semester.SEMESTER):
                if week <= self.getMaxWeekInSemester():
                    Semester.SEMESTER_INDEX = week-1
                    self.signal_indexChanged.emit(Semester.SEMESTER_INDEX)