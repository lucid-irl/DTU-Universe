import re
from typing import List, Set, Text
from bs4 import BeautifulSoup
from bs4.element import Tag
from cleanSubTime import clean_SubTime, get_list_schedule_raw_from_html
from cs4rsa_helpfulFunctions import *

import requests
import os
import sys
import json

class SubjectPage:
    """Class này chịu trách nhiệm lấy URL HTML raw của một Subject page nào đó.
    Ngoài ra nó còn có các phương thức chức năng để giải quyết các vấn đề về lưu file HTML và kiểm tra lịch học."""

    def __init__(self, semester: int) -> None:
        self.semester = semester

    @staticmethod
    def __extractCourseId(url: str):
        """Tách course id từ url."""
        params = re.findall(r'=(.*?)&', url)
        return params[1]

    @staticmethod
    def toFile(url: str, filename: str):
        """Lấy HTML của một URL truyền vào và ghi ra một file."""
        r = requests.get(url)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(r.text)

    @staticmethod
    def isHaveSchedule(url):
        """Kiểm tra xem một URL tới trang HTML raw của Subject nào đó có lịch lớp học hay không. 
        Nếu có trả về True, ngược lại trả về False."""
        htmlPage = requests.get(url).text
        soup = BeautifulSoup(htmlPage, 'lxml')
        if soup.find('span', {'class':'title','style':'color: #990000'}):
            return False
        return True

    def getSubjectUrl(self, discipline: str, keyword1: str):
        """Trả về đường dẫn tới trang HTML raw của Subject.
        
        >>> sp = SubjectPage(70)
        >>> sp.getSubjectUrl('CS','414')
        """
        params = {
            'discipline': discipline,
            'keyword1': keyword1,
            'hocky': self.semester,
        }
        courseResultSearchUrl = 'http://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx'
        page = requests.get(courseResultSearchUrl, params).text
        soup = BeautifulSoup(page,'lxml')
        urlSub = soup.find_all(class_='hit')[2]['href'] 
        courseId = SubjectPage.__extractCourseId(urlSub)

        urlOutput = "http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid={0}&semesterid={1}&timespan={2}"
        return urlOutput.format(courseId, self.semester, self.semester)


class RawClass:
    """Class này đại diện cho một hàng trong bảng lịch học bao gồm các thông tin."""

    def __init__(self, className, registerCode, type, emptySeat,
                registrationTermStart, registrationTermEnd, 
                weekStart, weekEnd,
                hour, rooms, locations, 
                teachers:Set[str], registrationStatus, implementationStatus) -> None:
        self.__className = className
        self.__registerCode = registerCode
        self.__type = type
        self.__emptySeat = emptySeat
        self.__registrationTermStart = registrationTermStart
        self.__registrationTermEnd = registrationTermEnd
        self.__weekStart = weekStart
        self.__weekEnd = weekEnd
        self.__hour = hour
        self.__rooms = rooms
        self.__locations = locations
        self.__teachers = teachers
        self.__registrationStatus = registrationStatus
        self.__implementationStatus = implementationStatus
    
    @property
    def className(self):
        return self.__className

    @property
    def registerCode(self):
        return self.__registerCode

    @property
    def type(self):
        return self.__type

    @property
    def teachers(self):
        return self.__teachers

    @teachers.setter
    def teachers(self, teachers: List[str]):
        self.__teachers = teachers

    def __str__(self) -> str:
        return '<RawClass {0}>'.format(self.__className)

    def __repr__(self) -> str:
        return '<RawClass {0}>'.format(self.__className)

    def getJson(self):
        return {
            "class_name" : self.__className,
            "register_code" : self.__registerCode,
            "type" : self.__type,
            "empty_seat" : self.__emptySeat,
            "registration_term_start" : self.__registrationTermStart,
            "registration_term_end" : self.__registrationTermEnd,
            "week_start" : self.__weekStart,
            "week_end" : self.__weekEnd,
            "hour" : self.__hour,
            "room" : self.__rooms,
            "location" : self.__locations,
            "teacher" : self.__teachers,
            "registration_status" : self.__registrationStatus,
            "implementation_status" : self.__implementationStatus
        }

    def isHaveRegisterCode(self):
        """Trả về True nếu môn này có register code, ngược lại trả về False."""
        return True if self.__registerCode != "" else False

    def setRegisterCode(self, registerCode:str):
        self.__registerCode = registerCode

    def addTeacher(self, teacher: str):
        self.__teachers.add(teacher)


class ClassGroup:
    """Đại diện cho một Nhóm lớp chứa các lớp có cùng mã đăng ký."""

    def __init__(self, name: str, rawClasses: List[RawClass]=[]) -> None:
        """@name: tên của nhóm lớp
        
        @rawClasses: List các RawClasses."""
        self.__name = name
        self.__rawClasses = rawClasses
        self.shareRegisterCode()
        self.mergeTeacherRawClassAndSet()

    def __len__(self):
        return len(self.__rawClasses)

    def __str__(self) -> str:
        return '<ClassGroup {0}>'.format(self.__name)

    def __repr__(self) -> str:
        return '<ClassGroup {0}>'.format(self.__name)

    def __isSameName(rawClasses: List[RawClass]) -> bool:
        """@rawClasses: Một list các RawClass
        
        Hàm này kiểm tra xem các RawClass trong list đó có cùng tên hay không."""
        for i in range(len(rawClasses)):
            if i == len(rawClasses)-1:
                return True
            if rawClasses[i].className == rawClasses[i+1].className:
                continue
        return False

    def getName(self) -> str:
        return self.__name

    def getRawClasses(self) -> List[RawClass]:
        return self.__rawClasses

    def howMuchRawClass(self, className: str):
        """"""

    def getRawClassNames(self):
        return set(rawClass.className for rawClass in self.__rawClasses)

    def mergeTeacherRawClass(self, rawClasses: List[RawClass]) -> RawClass:
        if ClassGroup.__isSameName(rawClasses):
            teachers = []
            for rawClass in rawClasses:
                teachers.extend(rawClass.teachers)
            rawClasses[0].teachers = teachers
            return rawClasses[0]
        else:
            print("Can not merge")

    def mergeTeacherRawClassAndSet(self):
        """Trả về một danh sách các RawClass đã được gộp.
        
        Trong một nhóm lớp sẽ có khả năng có những lớp với nhiều giảng viên dạy vì thế việc gộp là cần thiết."""
        listRawClassSet = []
        for rawClassName in self.getRawClassNames():
            listRawClass = [rawClass for rawClass in self.getRawClasses() if rawClass.className == rawClassName]
            rawClass = self.mergeTeacherRawClass(listRawClass)
            listRawClassSet.append(rawClass)
        self.__rawClasses = listRawClassSet

    def shareRegisterCode(self):
        """Đổ register code cho toàn bộ RawClass có trong Nhóm lớp."""
        if self.isHaveManyRegisterCode():
            print('Can not share')
        else:
            registerCode = self.getRegisterCodes()[0]
            for rawClass in self.__rawClasses:
                rawClass.setRegisterCode(registerCode)


    def getJson(self):
        pass

    def getRegisterCodes(self):
        """Trả về một list chứa register code của group này."""
        return [rawClass.registerCode for rawClass in self.__rawClasses if rawClass.isHaveRegisterCode()]

    def addRawClass(self, rawClass: RawClass):
        """Thêm một RaWClass vào ClassGroup."""
        self.__rawClasses.append(rawClass)

    def isHaveManyRegisterCode(self):
        """Nếu một nhóm lớp có nhiều hơn một mã đăng ký thì mặc định ứng dụng sẽ cho đây là một
        môn học đặc biệt và không sử dụng môn này.
        
        Phương thức này để kiểm tra môn học có phải là môn học đặc biệt hay không thông qua số lượng
        mã đăng ký mà một nhóm lớp chứa."""
        return True if len(self.getRegisterCodes()) >= 2 else False


class SubjectData:
    """Class này sẽ tách data từ một HTML page ra thành một cây JSON có cấu trúc."""

    def __init__(self, htmlPage: str):
        self.__soup = BeautifulSoup(htmlPage, 'lxml')

    def getListClassGroupName(self):
        """Trả về một list là tên các nhóm lớp."""
        table = self.__soup.find_all('table', class_='tb-calendar')
        listTdGroupClass = table[0]('tbody')[0]('td', class_='nhom-lop')
        listClassGroup = []
        for tdTag in listTdGroupClass:
            groupClassName = str(tdTag.div.text).strip()
            listClassGroup.append(groupClassName)
        return listClassGroup

    @staticmethod
    def __cleanFilterRoom(item):
        """Filter các item trong list các Phòng học."""
        if item == '<br/>' or item == '':
            return False
        return True

    @staticmethod
    def __cleanEmptySeat(tdTag: Tag) -> int:
        """Nhận vào một tdTag của Chỗ ngồi và trả về số chỗ ngồi còn lại."""
        if tdTag.div:
            if toStringAndCleanSpace(tdTag.div.text) == 'Hết chỗ':
                return 0
            return int(toStringAndCleanSpace(tdTag.div.text))
        return int(toStringAndCleanSpace(tdTag.text))

    def getRawClass(self, trTag: Tag) -> RawClass:
        """Nhận vào một <tr class='lop'> và trả về một RawClass."""
        listTdTagInTrTag = trTag('td')
        name = toStringAndCleanSpace(trTag.td.a.text)
        registerCode = toStringAndCleanSpace(listTdTagInTrTag[1].a.text) if listTdTagInTrTag[1].a.text else ""
        type = toStringAndCleanSpace(listTdTagInTrTag[2].text)
        emptySeat = self.__cleanEmptySeat(listTdTagInTrTag[3])
        registrationTermStart = toStringAndCleanSpace(listTdTagInTrTag[4]('div')[0].text)
        registrationTermEnd = toStringAndCleanSpace(listTdTagInTrTag[4]('div')[1].text)
        weekStart = toStringAndCleanSpace(listTdTagInTrTag[5].text).split('--')[0]
        weekEnd = toStringAndCleanSpace(listTdTagInTrTag[5].text).split('--')[1]
        hours = clean_SubTime(str(listTdTagInTrTag[6]))
        rooms = list(filter(self.__cleanFilterRoom,[toStringAndCleanSpace(i) for i in listTdTagInTrTag[7].contents]))
        locations = list(set(filter(self.__cleanFilterRoom,[toStringAndCleanSpace(i) for i in listTdTagInTrTag[8].contents])))
        teachers = [toStringAndCleanSpace(listTdTagInTrTag[9].text)]
        registrationStatus = toStringAndCleanSpace(listTdTagInTrTag[10].font.text)
        implementationStatus = toStringAndCleanSpace(listTdTagInTrTag[11].div.text)
        return RawClass(name, registerCode, type, emptySeat, registrationTermStart, 
                        registrationTermEnd, weekStart, weekEnd, hours, rooms, locations,
                        teachers, registrationStatus, implementationStatus)
        
    def getListRawClass(self, listTrTag:List[Tag]) -> List[RawClass]:
        return [self.getRawClass(trTag) for trTag in listTrTag]

    def getListClassGroup(self) -> List[ClassGroup]:
        """Trả về một list các ClassGroup."""
        table = self.__soup.find_all('table', class_='tb-calendar')
        listTrTag = table[0]('tr',class_='lop')
        listClassGroup = []
        for groupName in self.getListClassGroupName():
            ListRawClassPass = list(rawClass for rawClass in self.getListRawClass(listTrTag) if rawClass.className[0: len(groupName)] == groupName)
            classGroup = ClassGroup(groupName, ListRawClassPass)
            listClassGroup.append(classGroup)
        return listClassGroup

    def getJson(self):
        if self.isNormalSubject():
            pass

    def isNormalSubject(self):
        """Kiểm tra xem môn học này có phải là một môn học bình thường không.
        
        Một môn được xem là một môn học bình thương sẽ chỉ có một mã đăng ký trong một nhóm lớp."""
        for classGroup in self.getListClassGroup():
            if classGroup.isHaveManyRegisterCode():
                return False
        return True
        



with open('me_PMY_302.html','r', encoding='utf-8') as f:
    gr = SubjectData(f.read()).getListClassGroup()[0]

    print(gr.getRawClasses()[0].teachers)
