"""Class Subject Crawler
~~~~~~~~~~~~~~~~~~~~~~~~
Chuyển dữ liệu từ HTML sang JSON."""

from class_schedule import Schedule
from class_subject import Subject, indexOfLecLab, isHaveLecLab, mergeListSubject, mergeTwoSubject
from typing import Dict, List, Set, Text
from bs4 import BeautifulSoup
from bs4.element import Tag
from cs4rsa_cleanSubTime import cleanScheduleTime
from cs4rsa_helpfulFunctions import *

import re
import requests
import json


class ExceptionNotHaveSchedule(Exception):
    def __init__(self, subjectCode) -> None:
        self.message = '{0} have not schedule in this semester.'.format(subjectCode)
        super().__init__(self.message)

class ExceptionNotHaveRegisterCode(Exception):

    def __init__(self, name) -> None:
        self.message = 'ClassGroup {0} have not register code'.format(name)
        super().__init__(self.message)

class ExceptionSpecialSubject(Exception):

    def __init__(self, name) -> None:
        self.message = """{0} is a special subject. 
        Can not share register code in this class group because it have many one.""".format(name)
        super().__init__(self.message)

class ExceptionCantFoundThisSubject(Exception):

    def __init__(self, subjectName: str) -> None:
        self.message = 'Could not find this subject {0}'.format(subjectName)
        super().__init__(self.message)

class SubjectPage:
    """Class này đại diện cho một course detail page bao gồm các thông tin về lịch lớp học.
    Đảm bảo một request duy nhất tới server DTU.
    """

    def __init__(self, currentSemesterValue: str, discipline: str, keyword1: str):
        super(SubjectPage, self).__init__()
        self.currentSemesterValue = currentSemesterValue
        self.discipline = discipline
        self.keyword1 = keyword1
        self.subjectCode = discipline+' '+keyword1
        # check here
        self.url = self.getSubjectUrl(self.discipline, self.keyword1)
        self.htmlPage = requests.get(self.url).text
        self.soup = BeautifulSoup(self.htmlPage, 'lxml')
        self.haveSchedule = self.isHaveSchedule()

    def __str__(self):
        return '<SubjectPage SemesterID: {2} {0} {1}>'.format(self.discipline, self.keyword1, self.currentSemesterValue)

    def getUrl(self):
        return self.url
    
    def getSoup(self):
        return self.soup
    
    def getIsHaveSchedule(self):
        return self.haveSchedule

    @staticmethod
    def extractCourseId(url: str):
        """Tách course id từ url."""
        params = re.findall(r'=(.*?)&', url)
        return params[1]

    def isHaveSchedule(self):
        """Kiểm tra xem một URL tới trang HTML raw của Subject nào đó có lịch lớp học hay không. 
        Nếu có trả về True, ngược lại trả về False."""
        if self.soup.find('span', {'class':'title','style':'color: #990000'}):
            raise ExceptionNotHaveSchedule(self.subjectCode)
        return True

    def getSubjectUrl(self, discipline: str, keyword1: str):
        """Trả về đường dẫn tới trang HTML raw của Subject.
        >>> sp = SubjectPage(70)
        >>> sp.getSubjectUrl('CS','414')
        """
        params = {
            'discipline': discipline,
            'keyword1': keyword1,
            'hocky': self.currentSemesterValue,
        }
        courseResultSearchUrl = 'http://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx'
        r = requests.get(courseResultSearchUrl, params)
        page = r.text
        soup = BeautifulSoup(page,'lxml')
        hitTag = soup.find_all(class_='hit')
        if hitTag:
            urlSub = hitTag[1]['href']
            courseId = SubjectPage.extractCourseId(urlSub)
            urlOutput = "http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid={0}&semesterid={1}&timespan={2}"
            return urlOutput.format(courseId, self.currentSemesterValue, self.currentSemesterValue)
        else:
            raise ExceptionCantFoundThisSubject(discipline+' '+keyword1)

    def toFile(self, filename: str=None):
        """Lấy HTML của một URL truyền vào và ghi ra một file."""
        r = requests.get(self.url)
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(r.text)
        else:
            with open(self.getName()+'.html', 'w', encoding='utf-8') as f:
                f.write(r.text)

    def getSubjectCode(self) -> str:
        """Trả về mã môn."""
        return self.discipline +' '+ self.keyword1

    def getName(self) -> str:
        """Trả về tên môn."""
        name = self.getSoup().find('span').text
        return toStringAndCleanSpace(name)

    def getCredit(self) -> int:
        """Trả về số lượng đơn vị học tập của môn này được tính bằng tín chỉ."""
        """//*[@id="ResultCourseClass"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]"""
        table = self.getSoup().find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[1]('td')[1]
        credit = int(toStringAndCleanSpace(tdTag.text).split(' ')[0])
        return credit

    def getDetailCreditList(self) -> List:
        """Phân rã chi tiết số đơn vị học tập."""
        table = self.getSoup().find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[1]('td')[1]
        text = toStringAndCleanSpace(tdTag.text)
        listStringCreditDetail = getListStringMatchRegex(text, r'([0-9]*[A-Z]*)')
        listStringCreditDetail.pop(0)
        return listStringCreditDetail

    def getDetailCreditString(self) -> List:
        """Lấy mô tả số ĐVHT."""
        table = self.getSoup().find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[1]('td')[1]
        credit = toStringAndCleanSpace(tdTag.text)
        return credit

    def getStudyUnitType(self):
        table = self.soup.find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[2]('td')[1]
        text = toStringAndCleanSpace(tdTag.text)
        return text

    def getStudyType(self):
        table = self.soup.find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[3]('td')[1]
        text = toStringAndCleanSpace(tdTag.text)
        return text

    def getSemester(self):
        table = self.soup.find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[4]('td')[1]
        text = toStringAndCleanSpace(tdTag.text)
        return text

    def getMustStudySubject(self):
        """Môn học tiên quyết."""
        table = self.soup.find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[5]('td')[1]
        text = toStringAndCleanSpace(tdTag.font.text)
        return text

    def getParallelSubject(self):
        """Môn học song hành."""
        table = self.soup.find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[6]('td')[1]
        text = toStringAndCleanSpace(tdTag.font.text)
        return text

    def getDescription(self):
        """Mô tả môn học."""
        table = self.soup.find('table', class_='tb_coursedetail')
        tdTag = table('table')[0]('tr')[7]('td')[1]
        text = toStringAndCleanSpace(tdTag.text)
        return text


class RawClass:
    """Class này đại diện cho một hàng trong bảng lịch học bao gồm các thông tin."""

    def __init__(self, className, registerCode: str, type, emptySeat,
                registrationTermStart, registrationTermEnd, 
                weekStart, weekEnd,
                hour: List[Dict[str, List]], rooms, locations, 
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
            "week_start" : int(self.__weekStart),
            "week_end" : int(self.__weekEnd),
            "hour" : self.__hour,
            "rooms" : self.__rooms,
            "locations" : self.__locations,
            "teachers" : self.__teachers,
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

    def toSubject(self, name: str, credit: int, detailCredit: List) -> Subject:
        """
        Bản thân RawClass đại diện cho một row trong bảng danh sách lớp đăng ký
        nên nó sẽ còn thiếu một số trường sau.

        @name: Tên môn học, ví dụ Lập trình hướng đối tượng.
        
        @credit: Số tín chỉ"""
        return Subject(
            self.__registerCode, self.__className, name,
            credit, detailCredit, self.__emptySeat, self.__type, Schedule(self.__hour),
            self.__teachers, self.__locations, self.__rooms, int(self.__weekStart),
            int(self.__weekEnd), self.__registrationTermStart, self.__registrationTermEnd,
            self.__registrationStatus, self.__implementationStatus
        )

class ClassGroup:
    """Đại diện cho một Nhóm lớp chứa các lớp có cùng mã đăng ký."""

    def __init__(self, name: str, rawClasses: List[RawClass]=[]) -> None:
        """@name: tên của nhóm lớp
        
        @rawClasses: List các RawClasses."""
        self.__name = name
        self.__rawClasses = rawClasses
        if self.isHaveManyRegisterCode():
            raise ExceptionSpecialSubject(self.__name)
        else:
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
        return list({rawClass.getRegisterCode() for rawClass in self.__rawClasses if rawClass.isHaveRegisterCode()})

    @staticmethod
    def mergeTeacherRawClass(rawClasses: List[RawClass]) -> RawClass:
        if ClassGroup.__isSameName(rawClasses):
            teachers = []
            for rawClass in rawClasses:
                teachers.extend(rawClass.getTeachers())
            rawClasses[0].setTeachers(teachers)
            return rawClasses[0]
        else:
            raise Exception("Can not merge: each item in list of rawclass must same name one by one!!!")

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
        if self.isHaveOnlyOneRegisterCode():
            registerCode = self.getRegisterCodes()[0]
            for rawClass in self.__rawClasses:
                rawClass.setRegisterCode(registerCode)

    def isHaveManyRegisterCode(self):
        """Nếu nhóm lớp này có nhiều mã đăng ký nó sẽ trả về True ngược lại trả về False."""
        return True if len(self.getRegisterCodes()) > 1 else False

    def isNotHaveRegisterCode(self):
        """Nếu môn này không có mã đăng ký nào nó sẽ trả về True ngược lại trả về False."""
        return True if len(self.getRegisterCodes()) == 0 else False

    def isHaveOnlyOneRegisterCode(self):
        """Trả về True nếu Nhóm Lớp này có đúng một mã đăng ký."""
        return True if len(self.getRegisterCodes()) == 1 else False

    def isHaveRegisterCode(self):
        return True if len(self.getRegisterCodes()) >= 1 else False

    def addRawClass(self, rawClass: RawClass):
        """Thêm một RaWClass vào ClassGroup."""
        self.__rawClasses.append(rawClass)

class SubjectData:
    """Class này sẽ trích xuất data có trong một SubjectPage để lấy ra thông tin của môn học.

    Class này có các signal sau cần được connect với các slot để xử lý các behavior tương ứng."""

    def __init__(self, subjectPage: SubjectPage):
        """@subjectPage: Một SubjectPage đã thực hiện phương thức run() của nó."""
        self.__subjectCode = subjectPage.getSubjectCode() 
        self.__name = subjectPage.getName()
        self.__credit = subjectPage.getCredit()
        self.__creditDetail = subjectPage.getDetailCreditList()

        self.creditString = subjectPage.getDetailCreditString()
        self.studyUnitType = subjectPage.getStudyUnitType()
        self.semester = subjectPage.getSemester()
        self.studyType = subjectPage.getStudyType()
        self.mustStudySubject = subjectPage.getMustStudySubject()
        self.parallelSubject = subjectPage.getParallelSubject()
        self.description = subjectPage.getDescription()
        self.__soup = subjectPage.getSoup()

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
        listRawClassNonFilter = self.__getListRawClass(listTrTag)

        listClassGroup = []
        for groupName in self.getListClassGroupName():
            classGroupNotYetSharingRegisterCode = SubjectData.filterAClassGroup(groupName, listRawClassNonFilter)
            if classGroupNotYetSharingRegisterCode.isHaveRegisterCode():
                if classGroupNotYetSharingRegisterCode.isHaveOnlyOneRegisterCode():
                    listClassGroup.append(classGroupNotYetSharingRegisterCode)
                    # important !!!
                    classGroupNotYetSharingRegisterCode.shareRegisterCode()
        return listClassGroup

    @staticmethod
    def filterAClassGroup(classGroupName: str, rawClasses: List[RawClass]) -> ClassGroup:
        """Trả về một ClassGroup có sỡ hữu các RawClass có tên giống tên của nó. 
        #### ClassGroup này chưa thực hiện sharing Register Code.
        Nếu không có RawClass nào thoả mãn sẽ trả về một list rỗng.
        
        @classGroupName: Tên của một ClassGroup.
        @rawClasses: Danh sách các RawClass chưa được lọc."""
        def cleanFilterClassGroup(rawClass: RawClass):
            pattern = '^({0}[0-9]*)$'.format(classGroupName)
            if re.search(pattern, rawClass.getClassName()):
                return True
            return False

        listRawClassPass = list(filter(cleanFilterClassGroup, rawClasses))
        return ClassGroup(classGroupName, listRawClassPass)

    @staticmethod
    def isHaveRegisterCode(rawClassPasses: List[RawClass]):
        """Kiểm tra xem list chứa các RawClass có mã đăng ký hay không.
        
        Khi nào tìm thấy một mã đăng ký trong list này trả về True, ngược lại trả về False.
        
        @rawClassPasses: List of RawClass. Will be used in getListClassGroup() method."""
        for rawClass in rawClassPasses:
            if rawClass.isHaveRegisterCode():
                return True
        return False

    def getJson(self):
        """Trả về thông tin dưới dạng JSON đầy đủ của môn học được tìm kiếm."""
        jsonOut = {
            'name':self.__name,
            'credit_string':self.creditString,
            'credit': self.__credit, 
            'credit_detail': self.__creditDetail,
            'subject_code': self.__subjectCode,
            'study_unit_type': self.studyUnitType,
            'study_type': self.studyType,
            'semester': self.semester,
            'must_study_subject': self.mustStudySubject,
            'parallel_subject':self.parallelSubject,
            'description':self.description}
        for classGroup in self.getListClassGroup():
            jsonOut.update(classGroup.getJson())
        return jsonOut

    def getJsonNonIncludeName(self):
        """Lấy ra JSON không bao gồm tên môn học."""
        jsonOut = {}
        for classGroup in self.getListClassGroup():
            jsonOut.update(classGroup.getJson())
        return jsonOut

    def toJsonFile(self):
        with open(self.getSubjectCode()+'.json', 'w', encoding='utf-8') as f:
            json.dump(self.getJson(),f, ensure_ascii=False, indent=4)    
        
    def getSubjects(self) -> List[Subject]:
        """Trả về một list các Subject."""
        subjectsOut = []
        for classGroup in self.getListClassGroup():
            rawClasses = classGroup.getRawClasses()
            subjectsInClassGroup = [rawClass.toSubject(self.__name, self.__credit, self.__creditDetail) for rawClass in rawClasses]
            subjectsOut.extend(subjectsInClassGroup)
        return subjectsOut

if __name__ == "__main__":
    sp = SubjectPage('70','CS','414')
    sd = SubjectData(sp)
    sjs = sd.getSubjects()
    listSubject = [sjs[0], sjs[1]]