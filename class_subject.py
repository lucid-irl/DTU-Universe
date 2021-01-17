import logging
from typing import Dict, List, Tuple
from class_schedule import Schedule
import re
import json


class ColorError(Exception):

    def __init__(self, color: str) -> None:
        self.color = color
        self.message = '{0} is Error :D'.format(self.color)
        super().__init__(message=self.message)

class Subject:
    """Đại diện cho một môn học trong một học kỳ."""

    def __init__(self, registerCode: str, subjectCode: str, name: str, credit: int, creditDetail: List, emptySeat: int, type:str,
                schedule: Schedule, teachers: List[str], locations: List[str], rooms:List[str],
                weekStart: int, weekEnd: int, 
                registrationTermStart: str, registrationTermEnd:str, 
                registrationStatus: str, implementationStatus:str):
        """
        @registerCode: Mã đăng ký lớp học.

        @subjectCode: Mã lớp học.

        @number_of_seats_left: Số chỗ còn lại.

        @credits: Số tín chỉ.

        @schedule: Một Schedule object đại diện cho thời gian của môn đó trong một Tuần học.

        @teachers: Một list các tên giảng viên.

        @locations: Nơi học.

        @rooms: Phòng học.

        @week_start: Tuần bắt đầu.

        @week_end: Tuần kết thúc.

        @registration_status: Tình trạng đăng ký.

        @implementation_status: Tình trạng triển khai.

        @name: Tên của môn học.
        
        @type: Loại hình môn học LEC/LAB/DEM/...
        
        @registration_term_start: Ngày bắt đầu đăng ký

        @registration_term_end: Ngày kết thúc đăng ký"""

        self.registerCode = registerCode
        self.subjectCode = subjectCode
        self.name = name
        self.emptySeat = emptySeat  
        self.credit = credit
        self.creditDetail = creditDetail
        self.type = type

        self.schedule = schedule
        self.teachers = teachers
        self.locations = locations
        self.rooms = rooms
        self.weekStart = weekStart
        self.weekEnd = weekEnd

        self.registrationTermStart = registrationTermStart
        self.registrationTermEnd = registrationTermEnd

        self.registrationStatus = registrationStatus
        self.implementationStatus = implementationStatus
        
        self.color = None


    def __str__(self):
        return "<Subject {0}>".format(self.subjectCode)

    def __repr__(self) -> str:
        return "<Subject {0}>".format(self.subjectCode)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Subject):
            return self.registerCode == o.registerCode

    def getLocations(self):
        return self.locations

    def setColor(self, color: str):
        if re.match(r'^#(?:[0-9a-f]{3}){1,2}$', color):
            self.color = color
        else:
            raise ColorError(color)

    def getColor(self) -> str:
        return self.color

    def getSchedule(self) -> Schedule:
        return self.schedule

    def getName(self) -> str:
        return self.name
    
    def getRegistrationStatus(self) -> str:
        return self.registrationStatus

    def getRegisterCode(self) -> str:
        return self.registerCode

    def getSubjectCode(self):
        return self.subjectCode

    def getWeekStart(self):
        return self.weekStart

    def getWeekEnd(self):
        return self.weekEnd

    def getRooms(self):
        return self.rooms

    def getTeachers(self):
        return self.teachers

    def getType(self):
        return self.type

    def getEmptySeat(self):
        return self.emptySeat

    def getRegistrationTermStart(self):
        return self.registrationTermStart

    def getRegistrationTermEnd(self):
        return self.registrationTermEnd

    def getRegistrationStatus(self):
        return self.registrationStatus

    def getImplementationStatus(self):
        return self.implementationStatus

    def getCredit(self):
        return self.credit

    def getCreditDetail(self):
        return self.creditDetail

def comparingPairingSubject(pairingSubject1: Tuple[Subject], pairingSubject2: Tuple[Subject]):
    """So sánh hai ghép đôi Subject.
    
    Trả về True nếu hai ghép đôi như nhau, ngược lại trả về False."""
    if pairingSubject1[0] == pairingSubject2[0] and pairingSubject1[1] == pairingSubject2[1]:
        return True
    if pairingSubject1[0] == pairingSubject2[1] and pairingSubject1[1] == pairingSubject2[0]:
        return True
    return False

def isHaveThisPairingSubjectIn(listPairingSubject:List[Tuple[Subject]], pairingSubject: Tuple[Subject]):
    """Trả về True nếu một cặp các Subject có trong một list các cặp Subject."""
    for pairing in listPairingSubject:
        if comparingPairingSubject(pairing, pairingSubject):
            return True
    return False

def isIntersectWeek(subject1:Subject, subject2:Subject):
    """Hàm này dùng để xem xét khả năng xung đột của hai Subject.
    
    Trả về True nếu cả hai giao nhau về Tuần học, ngược lại trả về False."""
    logging.info('Subject intersect {} >< {}'.format(subject1, subject2))
    logging.info('Kiểm tra giao nhau trong tuần {}'.format([subject1.getWeekStart(), subject1.getWeekEnd(), subject2.getWeekStart(), subject2.getWeekEnd()]))
    weeks = [subject1.getWeekStart(), subject1.getWeekEnd(), subject2.getWeekStart(), subject2.getWeekEnd()]
    weeks.sort()
    if weeks[2] <= subject1.getWeekEnd():
        return True
    return False

def isIntersectWeek_Test(subject1:List, subject2:List):
    weeks = [subject1[0], subject1[1], subject2[0], subject2[1]]
    weeks.sort()
    if weeks[2] <= subject1[1]:
        return True
    return False

def fromJsonToSubjects(jsonData:Dict) -> List[Subject]:
    """Chuyển một JSON String thành một Subject."""
    subjects:List[Subject] = []
    name = jsonData['name']
    credit = jsonData['credit']
    creditDetail = jsonData['creditDetail']
    for classGroupCode, valueGroup in jsonData.items():
        for classCode, valueClass in valueGroup:
            className = valueClass['class_name']
            registerCode = valueClass['register_code']
            type = valueClass['type']
            emptySeat = valueClass['empty_seat']
            registrationTermStart = valueClass['registration_term_start']
            registrationTermEnd = valueClass['registration_term_end']
            weekStart = valueClass['week_start']
            weekEnd = valueClass['week_end']
            schedule = Schedule(valueClass['hour'])
            rooms = valueClass['rooms']
            locations = valueClass['locations']
            teachers = valueClass['teachers']
            registrationStatus = valueClass['registration_status']
            implementationStatus = valueClass['implementation_status']
            subject = Subject(registerCode, classCode, name, credit, emptySeat,
                            type, schedule, teachers, locations, rooms, weekStart,
                            weekEnd, registrationTermStart, registrationTermEnd, 
                            registrationStatus, implementationStatus)
            subjects.append(subject)
    return subjects


if __name__ == "__main__":
    pass