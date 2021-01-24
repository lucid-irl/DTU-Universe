"""Module này gồm các hàm lấy thông tin từ trang Home Course Search của MyDTU."""

from cs4rsa_helpfulFunctions import toStringAndCleanSpace
from class_DTUWeb import getTime
from typing import List
from bs4 import BeautifulSoup

import requests
import re
import json

class HomeCourseSearch:
    """Bao gồm các hàm chức năng giúp lấy ra các giá trị học kỳ và giá trị năm hiện tại của DTU."""

    @staticmethod
    def getSchoolYear():
        """Trả về một list chứa thông tin về giá trị năm học và thông tin năm học có dạng như sau.
        >>> [{'45': 'Năm Học 2014-2015'}, {'49': 'Năm Học 2015-2016'}]"""
        params = {
            't': getTime()
        }
        url = 'http://courses.duytan.edu.vn/Modules/academicprogram/ajax/LoadNamHoc.aspx?namhocname=cboNamHoc2&id=2'
        requestCourseSearch = requests.get(url, params=params)
        soup = BeautifulSoup(requestCourseSearch.text,'lxml')
        optionTags = soup.body.select('option')[1:]
        return [{optionTag['value']: toStringAndCleanSpace(optionTag.text)} for optionTag in optionTags]

    @staticmethod
    def getSemester(namhoc: str):
        """Hàm này nhận vào một chuỗi là giá trị năm học được lấy từ hàm shcoolYear(). 
        Và trả về một list học kỳ hiện có của năm học đó.

        @namhoc: năm học"""
        params = {
            'namhoc':namhoc
        }
        url ='http://courses.duytan.edu.vn/Modules/academicprogram/ajax/LoadHocKy.aspx?hockyname=cboHocKy1'
        requestCourseSearch = requests.get(url, params=params)
        soup = BeautifulSoup(requestCourseSearch.text,'lxml')
        optionTags = soup.body.select('option')[1:]
        return [{optionTag['value']: toStringAndCleanSpace(optionTag.text)} for optionTag in optionTags]

    @staticmethod
    def getCurrentSchoolYearValue() -> str:
        """Trả về giá trị năm học hiện tại."""
        return list(HomeCourseSearch.getSchoolYear()[-1].keys())[0]

    @staticmethod
    def getCurrentSchoolYearInfo():
        """Trả về thông tin năm học hiện tại."""
        return list(HomeCourseSearch.getSchoolYear()[-1].values())[0]

    @staticmethod
    def getCurrentSemesterValue() -> str:
        currentYearValue = HomeCourseSearch.getCurrentSchoolYearValue()
        return list(HomeCourseSearch.getSemester(currentYearValue)[-1].keys())[0]

    @staticmethod
    def getCurrentSemesterInfo() -> str:
        currentYearValue = HomeCourseSearch.getCurrentSchoolYearValue()
        return list(HomeCourseSearch.getSemester(currentYearValue)[-1].values())[0]

    @staticmethod
    def filterDuplicatesInDisciplines(disciplines):
        output = disciplines.copy()
        i = 0
        while not i == len(output)-1:
            j=i+1
            pattern = '({0})'.format(output[i])
            while not j == len(output)-1:
                if re.search(pattern, output[j]):
                    output.pop(j)
                else:
                    j+=1
            i+=1
        return output

    @staticmethod
    def getDisciplines():
        """Trả về list mã ngành có trùng lặp"""
        params = {
            't':getTime()
        }
        url = 'http://courses.duytan.edu.vn/Modules/academicprogram/ajax/LoadCourses.aspx?'
        requestCourseSearch = requests.get(url, params=params)
        soup = BeautifulSoup(requestCourseSearch.text,'lxml')
        soup = BeautifulSoup(requestCourseSearch.text,'lxml')
        optionTags = soup.body.select('option')[1:]
        return [optionTag['value'] for optionTag in optionTags]

    @staticmethod
    def getDisciplineFromFile(filename: str) -> List:
        with open(filename, 'r', encoding='utf-8') as f:
            jsonData = json.load(f)
        return jsonData

    @staticmethod
    def getFullDisciplineInfo(discipline, semester) -> List:
        """Lấy ra tất cả môn học liên quan tới mã ngành truyền vào."""
        params = {
            'discipline': discipline,
            'keyword1': '*',
            'hocky': semester,
            't': getTime()
        }
        url = 'http://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx'
        r = requests.get(url, params=params)
        soup = BeautifulSoup(r.text,'lxml')
        trTags = soup.tbody('tr', class_='lop')
        output = []
        for trTag in trTags:
            output.append(toStringAndCleanSpace(trTag.td.text)+' '+toStringAndCleanSpace(trTag('td')[1].text))
        return output

    @staticmethod
    def toFullInfoJson():
        disciplines = HomeCourseSearch.getDisciplines()
        disciplines = HomeCourseSearch.filterDuplicatesInDisciplines(disciplines)
        datas = []
        for dis in disciplines:
            data = HomeCourseSearch.getFullDisciplineInfo(dis, HomeCourseSearch.getCurrentSemesterValue())
            datas.extend(data)
        with open('allSubject.json', 'w', encoding='utf-8') as f:
            json.dump(datas, f, ensure_ascii=False)

    @staticmethod
    def getOnlyDisciplineInfo(discipline, semester) -> List:
        """Lấy ra tất cả môn học liên quan tới mã ngành truyền vào."""
        params = {
            'discipline': discipline,
            'keyword1': '*',
            'hocky': semester,
            't': getTime()
        }
        url = 'http://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx'
        r = requests.get(url, params=params)
        soup = BeautifulSoup(r.text,'lxml')
        trTags = soup.tbody('tr', class_='lop')
        output = []
        for trTag in trTags:
            output.append(toStringAndCleanSpace(trTag.td.text))
        return output

    @staticmethod
    def toDisciplineJson():
        disciplines = HomeCourseSearch.getDisciplines()
        disciplines = HomeCourseSearch.filterDuplicatesInDisciplines(disciplines)
        datas = []
        for dis in disciplines:
            datas.extend(HomeCourseSearch.getOnlyDisciplineInfo(dis, HomeCourseSearch.getCurrentSemesterValue()))
        with open('allDiscipline.json', 'w', encoding='utf-8') as f:
            json.dump(datas, f, ensure_ascii=False)

