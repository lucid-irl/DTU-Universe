from bs4 import BeautifulSoup
from bs4.element import Tag
import json


def getDivSemester(html : str) -> list:
    divSoup = BeautifulSoup(html, 'lxml')
    div_tag = divSoup.find_all('div', class_ = 'semeter')
    return div_tag

def getSemestersInfor(html : Tag) -> dict:
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
        'semester':semestersInfor,
        'subjects':listSubject
    }


if __name__ == "__main__":
    filename = "majors\Big Data & Machine Learning (Đại Học - HP).html"
    with open(filename,'r',encoding = 'utf-8') as f:
        data = f.read()
        listSemester = []
        for div in getDivSemester(data):
            listSemester.append(getSemestersInfor(div))
    with open('info.json','w',encoding='utf-8') as g:
        json.dump(listSemester, g, indent=4, ensure_ascii=False)
