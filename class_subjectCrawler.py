import re
from typing import List, Text
from bs4 import BeautifulSoup
from bs4.element import Tag
from cleanSubTime import clean_SubTime, get_list_schedule_raw_from_html
from cs4rsa_cleanData import *

import requests
import os
import sys
import json

class SubjectPage:

    def __init__(self, semester: int) -> None:
        self.semester = semester

    @staticmethod
    def toFile(url: str, filename: str):
        r = requests.get(url)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(r.text)

    @staticmethod
    def __extractCourseId(url: str):
        """Tách course id từ url."""
        params = re.findall(r'=(.*?)&', url)
        return params[1]

    @staticmethod
    def isHaveSchedule(url):
        """Kiểm tra xem một URL của Subject nào đó có lịch lớp học hay không. 
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

    def __init__(self, className, registerCode, type, emptySeat, registrationTermStart, registrationTermEnd, weekStart, weekEnd,
                hour, room, location, teacher, registrationStatus, implementationStatus) -> None:
        self.className = className
        self.registerCode = registerCode
        self.type = type
        self.emptySeat = emptySeat
        self.registrationTerm_start = registrationTermStart
        self.registrationTerm_end = registrationTermEnd
        self.week_start = weekStart
        self.week_end = weekEnd
        self.hour = hour
        self.room = room
        self.location = location
        self.teacher = teacher
        self.registrationStatus = registrationStatus
        self.implementationStatus = implementationStatus
    
    def getClassName(self):
        return self.className

    def __str__(self) -> str:
        return '<RawClass {0}>'.format(self.className)

    def __repr__(self) -> str:
        return '<RawClass {0}>'.format(self.className)


class ClassGroup:

    def __init__(self, name, rawClasses: List[RawClass]=[]) -> None:
        self.__name = name
        self.__rawClasses = rawClasses

    def isHaveLAB(self):
        pass

    def isHaveLEC(self):
        pass

    def addRawClass(self, rawClass: RawClass):
        self.__rawClasses.append(rawClass)

    def __len__(self):
        return len(self.__rawClasses)

    def __str__(self) -> str:
        return '<ClassGroup {0}>'.format(self.__name)

    def __repr__(self) -> str:
        return '<ClassGroup {0}>'.format(self.__name)

    @property
    def name(self):
        return self.__name

    @property
    def rawClasses(self):
        return self.__rawClasses



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

    def __cleanFilterRoom(self, item):
        """Filter các item trong list các Phòng học."""
        if item == '<br/>' or item == '':
            return False
        return True

    def __cleanEmptySeat(self, tdTag: Tag) -> int:
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
        hour = clean_SubTime(str(listTdTagInTrTag[6]))
        room = list(filter(self.__cleanFilterRoom,[toStringAndCleanSpace(i) for i in listTdTagInTrTag[7].contents]))
        location = set(filter(self.__cleanFilterRoom,[toStringAndCleanSpace(i) for i in listTdTagInTrTag[8].contents]))
        teacher = toStringAndCleanSpace(listTdTagInTrTag[9].text)
        registrationStatus = toStringAndCleanSpace(listTdTagInTrTag[10].font.text)
        implementationStatus = toStringAndCleanSpace(listTdTagInTrTag[11].div.text)
        return RawClass(name, registerCode, type, emptySeat, registrationTermStart, 
                        registrationTermEnd, weekStart, weekEnd, hour, room, location,
                        teacher, registrationStatus, implementationStatus)
        

    def getListClassGroup(self) -> List[ClassGroup]:
        """Trả về một list các ClassGroup đại diện cho một nhóm lớp với các môn LEC/LAB có mã môn thuộc nhau."""
        table = self.__soup.find_all('table', class_='tb-calendar')
        listTrTag = table[0]('tr',class_='lop')
        listClassGroup = []
        for groupName in self.getListClassGroupName():
            classGroup = ClassGroup(groupName)
            listClassGroup.append(classGroup)
        for trTag in listTrTag:
            rawClass = self.getRawClass(trTag)
            for group in listClassGroup:
                if re.search('^({0})'.format(group.name), rawClass.getClassName()):
                    group.addRawClass(rawClass)
                break
        return listClassGroup

        



with open('me_PMY_302.html','r', encoding='utf-8') as f:
    print(SubjectData(f.read()).getListClassGroup()[0].rawClasses)