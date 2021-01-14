import os
from bs4 import BeautifulSoup
from bs4.element import Tag
import json


def getDivSemester(html : str) -> list:
    divSoup = BeautifulSoup(html, 'lxml')
    div_tag = divSoup.find_all('div', class_ = 'semeter')
    return div_tag

def getSemestersInfor(html : Tag, id_) -> dict:
    semestersInfor = html.find('th', class_ = 'nobg nobd').text
    semestersInfor = str(semestersInfor).strip()
    tbody = html.find_all('tbody')[0]
    
    listTrTag = tbody('tr')
    
    listSubject = []
    for trTag in listTrTag:
        id = str(trTag('td')[0].a.text).strip()
        name = str(trTag('td')[1].a.text).strip()
        credit = str(trTag('td')[2].text).strip()
        subject = {'id':id, 'name':name,'credit':credit}
        listSubject.append(subject)
    return {
        'keyid':id_,
        'semester':semestersInfor,
        'subjects':listSubject
    }

def getHTMLFromFile(path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    majorHtmlPaths = ['majors/' + i for i in os.listdir('majors')]
    listMajor = []
    for k in range(len(majorHtmlPaths)):
        html = getHTMLFromFile(majorHtmlPaths[k])
        listSemesterDiv = getDivSemester(html)
        listInfoes = []
        for i in range(len(listSemesterDiv)):
            info = getSemestersInfor(listSemesterDiv[i], id_=i)
            listInfoes.append(info)
        major = majorHtmlPaths[k].split('/')[1].split('.')[0]
        
        listMajor.append({'id':k, 'major': major, 'semester_info':listInfoes})
    return listMajor

if __name__ == "__main__":

    js = main()
    with open('semester_info.json','w',encoding='utf-8') as g:
        json.dump(js, g, indent=4, ensure_ascii=False)