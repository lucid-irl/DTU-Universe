from typing import List
from class_schedule import Schedule
import re


class ColorError(Exception):

    def __init__(self, color: str) -> None:
        self.color = color
        self.message = '{0} is Error :D'.format(self.color)
        super().__init__(message=self.message)

class Subject:
    """Đại diện cho một môn học trong một học kỳ."""

    def __init__(self, registerCode: str, subjectCode: str, name: str, credits: int, emptySeat: int, type:str,
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

        @places: Nơi học.

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
        self.credits = credits
        self.type = type

        self.schedule = schedule
        self.teachers = teachers
        self.locations = locations
        self.rooms = rooms
        self.weekStart = weekStart
        self.weekEnd = weekEnd

        self.registrationTermStart = registrationTermStart
        self.registrationTermEnd = registrationTermEnd

        self.registration_status = registrationStatus
        self.implementation_status = implementationStatus
        
        self.color = None


    def __str__(self):
        return "<Subject {0}>".format(self.name)

    def __repr__(self) -> str:
        return "<Subject {0}>".format(self.name)

    def __eq__(self, o: object) -> bool:
        if self.name == o.name:
            return True
        else:
            return False

    def __cmp__(self, o: object):
        return cmp(self.registerCode, o.registerCode)

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
        return self.registration_status

    def getRegisterCode(self) -> str:
        return self.registerCode

    def getSubjectCode(self):
        return self.subjectCode

    def getWeekStart(self):
        return self.weekStart

    def getWeekEnd(self):
        return self.weekEnd