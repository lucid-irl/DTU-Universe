import logging
from team_config import UI_MAIN
from typing import Dict, List, Tuple
from class_schedule import Schedule

import cs4rsa_helpfulFunctions
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

    def getMaxWeek(self):
        """Trả về số tuần học tối đa."""
        return self.weekEnd-self.weekStart+1

    def setSubjectCode(self, subjectCode):
        self.subjectCode = subjectCode

    def setStudyType(self, type):
        self.type = type

    def setLocations(self, locations):
        self.locations = locations

    def setTeachers(self, teachers):
        self.teachers = teachers

    def toListInfo(self) -> List:
        """Đưa tất cả thông tin của Subject này thành một List."""
        registrationTerm = '{0} → {1}'.format(self.registrationTermStart, self.registrationTermEnd)
        studyWeek ='{} → {}'.format(self.weekStart,self.weekEnd)
        studyHours = self.schedule.fromScheduleToInfo()
        rooms = '\n'.join(self.rooms)
        places = '\n'.join(self.locations)
        teacher = '\n'.join(self.teachers)
        return [self.subjectCode, self.registerCode, self.type, 
                str(self.emptySeat), registrationTerm, studyWeek, 
                studyHours, rooms, places, teacher, self.registrationStatus, self.implementationStatus]

    def toDictInfoRenderExcel(self):
        """`(excel)` Đưa tất cả thông tin của Subject này thành một Dict."""
        registrationTerm = '{0} → {1}'.format(self.registrationTermStart, self.registrationTermEnd)
        studyWeek ='{} → {}'.format(self.weekStart,self.weekEnd)
        studyHours = self.schedule.fromScheduleToRenderExcel()
        rooms = ', '.join(self.rooms)
        places = ', '.join(self.locations)
        teachers = ', '.join(self.teachers)
        return {'register_code': self.registerCode, 
                'subject_code': self.subjectCode,
                'name': self.name,
                'empty_seat': str(self.emptySeat),
                'credit':self.credit, 
                'type':self.type, 
                'study_hours':studyHours,
                'teachers':teachers, 
                'places':places, 
                'rooms':rooms,
                'study_week':studyWeek, 
                'registration_term':registrationTerm, 
                'registration_status':self.registrationStatus, 
                'implementation_status':self.implementationStatus}

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

def isHaveInThisWeek(subject: Subject, week: int):
    """Nếu subject có tuần học trong tuần week thì trả về True ngược lại trả về False."""
    logging.info('isHaveInThisWeek {0} in week {1}'.format(subject, week))
    if week >= subject.getWeekStart() and week <= subject.getWeekEnd():
        return True
    return False

def isIntersectWeek(subject1:Subject, subject2:Subject):
    """Trả về True nếu hai Subject có tuần giao nhau, ngược lại trả về False."""
    weeks = [subject1.getWeekStart(), subject1.getWeekEnd(), subject2.getWeekStart(), subject2.getWeekEnd()]
    weeks.sort()
    if ((weeks[0] == subject1.getWeekStart() and weeks[1] == subject2.getWeekEnd()) or
        (weeks[0] == subject2.getWeekStart() and weeks[1] == subject2.getWeekEnd())):
        return False
    return True

def indexOfLecLab(subject: Subject, inList: List[Subject]) -> List:
    """Kiểm tra List of Subject truyền vào có Môn LEC hay LAB hay không. 
    Nếu có trả về list index của Subject LEC hoặc LAB tương ứng. Nếu không trả về None."""
    output = []
    i = 0
    while i<len(inList):
        if subject.getRegisterCode() == inList[i].getRegisterCode():
            output.append(i)
        i+=1
    return output

def intersectClassGroupName(subjectCode1, subjectCode2):
    """`(excel)` Hợp nhất hai subjectName để lấy được classGroupName."""
    output = ''
    if len(subjectCode1) > len(subjectCode2):
        for i in range(len(subjectCode2)):
            if subjectCode1[i] == subjectCode2[i]:
                output += subjectCode1[i]
    else:
        for i in range(len(subjectCode1)):
            if subjectCode1[i] == subjectCode2[i]:
                output += subjectCode1[i]
    return output

def isLecAndLab(subject1: Subject, subject2: Subject) -> bool:
    if (subject1.getRegisterCode() == subject2.getRegisterCode() and
        ((subject1.getType()=='LEC' or subject2.getType()=='LAB') or
        (subject1.getType()=='LAB' or subject2.getType()=='LEB'))):
        return True
    return False

def mergeTwoSubject(subject1: Subject, subject2: Subject):
    """`(excel)` Gộp hai Subject (LEC/LAB) thành một Subject."""
    if isLecAndLab(subject1, subject2):
        subjectCode = intersectClassGroupName(subject1.getSubjectCode(), subject2.getSubjectCode())
        studyType = '{0}/{1}'.format(subject1.getType(), subject2.getType())
        places = list(set(subject1.getLocations() + subject2.getLocations()))
        teachers = list(set(subject1.getTeachers() + subject2.getTeachers()))
        subject1.getSchedule().extend(subject2.getSchedule())

        subject1.setSubjectCode(subjectCode)
        subject1.setStudyType(studyType)
        subject1.setLocations(places)
        subject1.setTeachers(teachers)
        return subject1

def mergeListSubject(subjects: List[Subject]) -> Subject:
    """`(excel)` Gộp một List các Subject có cùng mã đăng ký lại thành một Subject duy nhất."""
    if len(subjects) < 2:
        return None
    output = subjects[0]
    while len(subjects) > 0:
        if len(subjects) > 1:
            subject = subjects.pop(1)
        else:
            subject = subjects.pop(0)
        if isLecAndLab(output, subject):
            output = mergeTwoSubject(output, subject)
            return output
        else:
            return None

def isHaveLecLab(subjects):
    subject1 = subjects[0]
    for i in range(1, len(subjects)):
        if subjects[i] == subject1:
            return True
    return False

def getTotalCredit(subjects: List[Subject]):
    output = 0
    for subject in subjects:
        output += subject.getCredit()
    return output

def reduceSubject(subjects: List[Subject]):
    """Gộp những lớp LEC/LAB lại với nhau và trả về một list Subject mới."""
    newSubjects: List[Subject] = []
    i = 0
    while len(subjects) > 0 and isHaveLecLab(subjects):
            indexs = indexOfLecLab(subjects[i], subjects)
            listSubjectLecLab: List[Subject] = cs4rsa_helpfulFunctions.getListObjectFromIndex(indexs, subjects)
            mergedSubject = mergeListSubject(listSubjectLecLab)
            newSubjects.append(mergedSubject)
            subjects = cs4rsa_helpfulFunctions.getNewListWithoutIndex(indexs, subjects)
    return newSubjects + subjects


def getWeekEndOfSubjects(subjects:List[Subject]):
    """Trả về tuần kết thúc của một list các Subject."""
    if subjects:
        maxWeekEnd = 0
        for subject in subjects:
            if subject.getWeekEnd() > maxWeekEnd:
                maxWeekEnd = subject.getWeekEnd()
        return maxWeekEnd
    return 0

def getWeekStartOfSubjects(subjects:List[Subject]):
    """Trả về tuần bắt đầu của một list các Subject."""
    if subjects:
        maxWeekStart = subjects[0].getWeekStart()
        for subject in subjects:
            if subject.getWeekStart() < maxWeekStart:
                maxWeekStart = subject.getWeekStart()
        return maxWeekStart
    return 0

def getMaxWeek(subjects:List[Subject]):
    """Trả về số tuần học tối đa của một danh sách các Subject."""
    if subjects:
        return getWeekEndOfSubjects(subjects) - getWeekStartOfSubjects(subjects) + 1
    return 0

def fromJsonToSubjects(jsonData:Dict) -> List[Subject]:
    """Chuyển một JSON String thành một list Subject."""
    subjects:List[Subject] = []
    name = jsonData['name']
    credit = jsonData['credit']
    for _, valueGroup in jsonData.items():
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


if __name__ == '__main__':
    print(intersectClassGroupName('cs 414 A', 'cs 414 A2123'))