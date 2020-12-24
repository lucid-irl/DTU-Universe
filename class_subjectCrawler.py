"""Class Subject Crawler
~~~~~~~~~~~~~~~~~~~~~~~~
Chuyển dữ liệu từ HTML sang JSON."""

import re
from typing import List, Set
from bs4 import BeautifulSoup
from bs4.element import Tag
from cleanSubTime import cleanScheduleTime
from cs4rsa_helpfulFunctions import *

import requests
import json


class SubjectPage:
    """Class này đại diện cho một course detail page bao gồm các thông tin về lịch lớp học.
    Đảm bảo một request duy nhất tới server DTU.
    
    I. Class này ngay sau khi khởi tạo nó sẽ gửi một request tới server DTU để kiểm tra xem:
    - Mã môn học có tồn tại hay không
    - Nếu có thì tiếp tục gửi request tới trang HTML raw và kiểm tra xem có lịch lớp học hay không
    
    II. Các phương thức sau sẽ có thể được gọi sau đó:
    - `toFile()` : Đưa SubjectPage thành một file HTML có tên như tên môn học
    - `getPage()` : Lấy ra chuỗi HTML.
    - `getSoup()`: Lấy ra soup được parse từ HTML."""

    def __init__(self, semester: int, discipline: str, keyword1: str) -> None:
        self.semester = semester
        self.discipline = discipline
        self.keyword1 = keyword1
        self.url = self.__getSubjectUrl(self.discipline, self.keyword1)
        self.htmlPage = None
        self.soup = None
        self.isHaveSchedule = self.__isHaveSchedule(self.url)

    @staticmethod
    def __extractCourseId(url: str):
        """Tách course id từ url."""
        params = re.findall(r'=(.*?)&', url)
        return params[1]

    def __isHaveSchedule(self, url):
        """Kiểm tra xem một URL tới trang HTML raw của Subject nào đó có lịch lớp học hay không. 
        Nếu có trả về True, ngược lại trả về False."""
        self.htmlPage = requests.get(url).text
        self.soup = BeautifulSoup(self.htmlPage, 'lxml')
        if self.soup.find('span', {'class':'title','style':'color: #990000'}):
            return False
        return True

    def __getSubjectUrl(self, discipline: str, keyword1: str):
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
        try:
            urlSub = soup.find_all(class_='hit')[2]['href'] 
            courseId = SubjectPage.__extractCourseId(urlSub)

            urlOutput = "http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid={0}&semesterid={1}&timespan={2}"
            return urlOutput.format(courseId, self.semester, self.semester)
        except:
            raise Exception('The subject code is wrong!!!')

    def getSoup(self) -> BeautifulSoup:
        return self.soup

    def getPage(self) -> str:
        """Trả về HTML của trang Class Raw."""
        if self.isHaveSchedule:
            return requests.get(self.url).text
        else:
            return None

    def toFile(self, filename: str=None):
        """Lấy HTML của một URL truyền vào và ghi ra một file."""
        r = requests.get(self.url)
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(r.text)
        else:
            with open(self.getName()+'.html', 'w', encoding='utf-8') as f:
                f.write(r.text)

    def getUrl(self):
        return self.url

    def getSubjectCode(self) -> str:
        return self.discipline +' '+ self.keyword1

    def getName(self) -> str:
        return toStringAndCleanSpace(self.soup.find('span').text)


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
    
    def getClassName(self) -> str:
        return self.__className

    def getRegisterCode(self):
        return self.__registerCode

    def getType(self):
        return self.__type

    def getTeachers(self):
        return self.__teachers

    def setTeachers(self, teachers: Set[str]):
        self.__teachers = teachers

    def __str__(self) -> str:
        return '<RawClass {0}>'.format(self.__className)

    def __repr__(self) -> str:
        return '<RawClass {0}>'.format(self.__className)

    def getJson(self):
        return {self.__className:{
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
        }}

    def isHaveRegisterCode(self):
        """Trả về True nếu môn này có register code, ngược lại trả về False."""
        return True if self.__registerCode else False

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
        self.mergeTeacherRawClassAndSet()
        self.shareRegisterCode()

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
            if rawClasses[i].getClassName() == rawClasses[i+1].getClassName():
                continue
        return False

    def getName(self) -> str:
        return self.__name

    def getRawClasses(self) -> List[RawClass]:
        return self.__rawClasses

    def getRawClassNames(self) -> Set[str]:
        return set(rawClass.getClassName() for rawClass in self.__rawClasses)

    def getJson(self):
        jsonOut = {}
        for rawClass in self.__rawClasses:
            jsonOut.update(rawClass.getJson())
        return {self.__name:jsonOut}

    def getRegisterCodes(self):
        """Trả về một list chứa register code của group này."""
        return [rawClass.getRegisterCode() for rawClass in self.__rawClasses if rawClass.isHaveRegisterCode()]

    @staticmethod
    def mergeTeacherRawClass(rawClasses: List[RawClass]) -> RawClass:
        if ClassGroup.__isSameName(rawClasses):
            teachers = []
            for rawClass in rawClasses:
                teachers.extend(rawClass.getTeachers())
            rawClasses[0].setTeachers(teachers)
            return rawClasses[0]
        else:
            print("Can not merge: each item in list of rawclass must same name one by one!!!")

    def mergeTeacherRawClassAndSet(self):
        """Trả về một danh sách các RawClass đã được gộp.
        
        Trong một nhóm lớp sẽ có khả năng có những lớp với nhiều giảng viên dạy vì thế việc gộp là cần thiết."""
        listRawClassSet = []
        for rawClassName in self.getRawClassNames():
            listRawClass = [rawClass for rawClass in self.getRawClasses() if rawClass.getClassName() == rawClassName]
            rawClass = ClassGroup.mergeTeacherRawClass(listRawClass)
            listRawClassSet.append(rawClass)
        self.__rawClasses = listRawClassSet

    def shareRegisterCode(self):
        """Đổ register code cho toàn bộ RawClass có trong Nhóm lớp."""
        if not self.isHaveManyRegisterCode():
            registerCode = self.getRegisterCodes()[0]
            for rawClass in self.__rawClasses:
                rawClass.setRegisterCode(registerCode)

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

    def __init__(self, htmlPage: str, subjectCode: str, name: str):
        self.__subjectCode = subjectCode 
        self.__name = name
        self.__soup = BeautifulSoup(htmlPage, 'lxml')

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

    def __getRawClass(self, trTag: Tag) -> RawClass:
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
        hours = cleanScheduleTime(str(listTdTagInTrTag[6]))
        rooms = list(filter(self.__cleanFilterRoom,[toStringAndCleanSpace(i) for i in listTdTagInTrTag[7].contents]))
        locations = list(set(filter(self.__cleanFilterRoom,[toStringAndCleanSpace(i) for i in listTdTagInTrTag[8].contents])))
        teachers = {toStringAndCleanSpace(listTdTagInTrTag[9].text)}
        registrationStatus = toStringAndCleanSpace(listTdTagInTrTag[10].font.text)
        implementationStatus = toStringAndCleanSpace(listTdTagInTrTag[11].div.text)
        return RawClass(name, registerCode, type, emptySeat, registrationTermStart, 
                        registrationTermEnd, weekStart, weekEnd, hours, rooms, locations,
                        teachers, registrationStatus, implementationStatus)
        
    def __getListRawClass(self, listTrTag:List[Tag]) -> List[RawClass]:
        return [self.__getRawClass(trTag) for trTag in listTrTag]

    def getSubjectCode(self) -> str:
        return self.__subjectCode

    def getName(self) -> str:
        return self.__name

    def getListClassGroupName(self) -> List[str]:
        """Trả về một list là tên các nhóm lớp."""
        table = self.__soup.find_all('table', class_='tb-calendar')
        listTdGroupClass = table[0]('tbody')[0]('td', class_='nhom-lop')
        listClassGroup = []
        for tdTag in listTdGroupClass:
            groupClassName = str(tdTag.div.text).strip()
            listClassGroup.append(groupClassName)
        return listClassGroup

    def getListClassGroup(self) -> List[ClassGroup]:
        """Trả về một list các ClassGroup."""
        table = self.__soup.find_all('table', class_='tb-calendar')
        listTrTag = table[0]('tr',class_='lop')
        listClassGroup = []
        for groupName in self.getListClassGroupName():
            ListRawClassPass = list(rawClass for rawClass in self.__getListRawClass(listTrTag) if rawClass.getClassName()[0: len(groupName)] == groupName)
            classGroup = ClassGroup(groupName, ListRawClassPass)
            listClassGroup.append(classGroup)
        return listClassGroup

    def getJson(self):
        jsonOut = {}
        for classGroup in self.getListClassGroup():
            jsonOut.update(classGroup.getJson())
        return jsonOut

    def toJsonFile(self):
        with open(self.getSubjectCode()+'.json', 'w', encoding='utf-8') as f:
            json.dump(self.getJson(),f, ensure_ascii=False, indent=4)    

    def isNormalSubject(self) -> bool:
        """Kiểm tra xem môn học này có phải là một môn học bình thường không.
        
        Một môn được xem là một môn học bình thương sẽ chỉ có một mã đăng ký trong một nhóm lớp."""
        for classGroup in self.getListClassGroup():
            if classGroup.isHaveManyRegisterCode():
                return False
        return True
        


if __name__ == "__main__":
    sp = SubjectPage(70,'PSU-FIN', '301')
    page = sp.getPage()
    sd = SubjectData(page, sp.getSubjectCode(), sp.getName())
    sd.toJsonFile()
