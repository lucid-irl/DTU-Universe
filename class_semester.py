from PyQt5.QtCore import QObject, pyqtSignal

from class_subject import Subject
from class_schedule import *
from class_conflict import *
from cs4rsa_color import *


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
    SEMESTER_INDEX = None
    SEMESTER_PAST_INDEX = 0

    signal_indexChanged = pyqtSignal('PyQt_PyObject')
    singal_addSubject = pyqtSignal('PyQt_PyObject')
    signal_deleteSubject = pyqtSignal('PyQt_PyObject')


    # IMPORTANT!!!
    def addSubject(self, subject: Subject):
        """Thêm một Subject vào Semester."""
        self.SUBJECTS.append(subject)
        self.__initSemester()
        self.__setSemesterIndex(0)
        self.singal_addSubject.emit(subject)

    def deleteSubject(self, subject: Subject):
        """Xoá một Subject khỏi Semester dựa theo ID."""
        self.SUBJECTS.remove(subject)
        self.__initSemester()
        self.__setSemesterIndex(0)
        self.signal_deleteSubject.emit(subject)


    # IMPORTANT!!!
    def __initSemester(self):
        """
        Phương thức này được tự động thực thi mỗi khi bạn thêm hoặc xoá Subject của Semester.\n
        Mỗi Subject sẽ có số Tuần học cụ thể từ Tuần nào tới Tuần nào. Vì thế lấy số Tuần tối đa mà Subject có thể chiếm. 
        Sau đó thực hiện đổ từ Subject tương ứng vào các List. Mỗi List sẽ đại diện cho một Tuần học.
        """
        self.SEMESTER = [[] for i in range(self.getMaxWeekInSemester())]
        for subject in self.SUBJECTS:
            for i in range(subject.getWeekStart()-1, subject.getWeekEnd()):
                self.SEMESTER[i].append(subject)
        return self.SEMESTER

    def getSubjects(self) -> List[Subject]:
        return self.SUBJECTS
    
    def getCurrentSubjects(self) -> List[Subject]:
        if len(self.SEMESTER) >0:
            return self.SEMESTER[self.SEMESTER_INDEX]
        

    def getWeek(self, week):
        """Phương thức này trả về một list các Subject trong một Tuần cụ thể của Semester. Nếu tuần đó không tồn tại
        phương thức này trả về một list rỗng."""
        if week < 0 or week >= self.SEMESTER_INDEX:
            return []
        else:
            return self.SEMESTER[week]

    def getConflicts(self) -> List[Conflict]:
        return self.__scanConflicts()

    def getPastIndex(self):
        return self.SEMESTER_PAST_INDEX

    # Các thao tác trên Semester
    def getCurrentSemesterIndex(self):
        return self.SEMESTER_INDEX

    def getTimeChains(self):
        return self.TIME_CHAINS
    
    def getMaxWeekInSemester(self) -> int:
        """Trả về số Tuần kéo dài tối đa mà Semester có thể có."""
        max = 0
        for subject in self.SUBJECTS:
            if subject.getWeekEnd() > max:
                max = subject.getWeekEnd()
        return max

    def scanSubjectConflict(self) -> List[List[Dict[str,Tuple[str]]]]:
        """
        **Không còn được dùng nữa**

        Bắt cặp tất cả Subject có trong danh sách trả về List chứa Conflicts.

        [[{'T6': ('9:15:00', '10:15:00')}, {'T6': ('7:00:00', '9:00:00')}, {'T6': ('7:00:00', '10:15:00')}]]
        """
        conflicts = []
        output = []
        tempSubjectsList = self.getCurrentSubjects().copy()
        while len(tempSubjectsList) > 1:
            baseSubject = tempSubjectsList[0]
            for i in range(1,len(tempSubjectsList)):
                if i==len(tempSubjectsList):
                    break
                conflict = Conflict(baseSubject, tempSubjectsList[i])
                if conflict.isConflict() and Semester.__isInConflict(conflict, conflicts) == False:
                    conflicts.append(conflict)
            tempSubjectsList.pop(0)
        for conflict in conflicts:
            output.append(conflict.getConflictTime())
        return output

    def __scanConflicts(self) -> List[Conflict]:
        """Trả về một list các Conflict có trong Semester."""
        conflicts = []
        for week in self.SEMESTER:
            tempSubjectsList = week.copy()
            while len(tempSubjectsList) > 1:
                baseSubject = tempSubjectsList[0]
                for i in range(1,len(tempSubjectsList)):
                    if i==len(tempSubjectsList):
                        break
                    conflict = Conflict(baseSubject, tempSubjectsList[i])
                    if conflict.getConflictTime() and Semester.__isInConflict(conflict, conflicts) == False:
                        conflicts.append(conflict)
                tempSubjectsList.pop(0)
        return conflicts

    def __setSemesterPastIndex(self, index: int):
        """Set giá trị cho biến giữ index trước đó của Semester."""
        self.SEMESTER_PAST_INDEX = index

    def __setSemesterIndex(self, index: int):
        self.SEMESTER_INDEX = index
        self.signal_indexChanged.emit(self.SEMESTER_INDEX)

    # Các phương thức về kiểm tra
    @staticmethod
    def __isInConflict(con: Conflict, listConflict: list) -> bool:
        for conflict in listConflict:
            if conflict == con:
                return True
        return False

    def __isValidIndex(self) -> bool:
        if self.SEMESTER_INDEX < len(self.SEMESTER) and self.SEMESTER_INDEX >= 0:
            return True
        else:
            return False


    # Điều khiển Week Context của Semester
    def nextWeek(self):
        """Phương thức này sẽ tăng index của Semester lên 1. Thao tác trên biến SEMESTER_INDEX."""
        if self.SEMESTER_INDEX >= 0 and self.SEMESTER_INDEX+1 < len(self.SEMESTER):
            self.__setSemesterPastIndex(self.SEMESTER_INDEX)
            if self.SEMESTER_INDEX < self.getMaxWeekInSemester():
                self.SEMESTER_INDEX+=1
                self.signal_indexChanged.emit(self.SEMESTER_INDEX)
                return self.SEMESTER_INDEX
            else:
                return -1

    def previousWeek(self):
        """Phương thức này sẽ giảm index của Semester xuống 1. Thao tác trên biến SEMESTER_INDEX."""
        if self.SEMESTER_INDEX-1 >= 0 and self.SEMESTER_INDEX < len(self.SEMESTER):
            self.__setSemesterPastIndex(self.SEMESTER_INDEX)
            if self.SEMESTER_INDEX > 0:
                self.SEMESTER_INDEX-=1
                self.signal_indexChanged.emit(self.SEMESTER_INDEX)
                return self.SEMESTER_INDEX
            else:
                return -1

    def gotoWeek(self, week: int) -> bool:
        if len(self.SEMESTER) > 0:
            if self.SEMESTER_INDEX >= 0 and self.SEMESTER_INDEX < len(self.SEMESTER):
                self.__setSemesterPastIndex(self.SEMESTER_INDEX)
                if week <= self.getMaxWeekInSemester():
                    self.SEMESTER_INDEX = week-1
                    self.signal_indexChanged.emit(self.SEMESTER_INDEX)
                    return week

