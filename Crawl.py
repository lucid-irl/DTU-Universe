from bs4 import BeautifulSoup
import requests
import json

from cleanSubTime import clean_SubTime


def Get_Url(discipline: str, keyword1: str) -> str:
    '''
    Trả về đường link source của môn học
    >>> Get_Url("ENG", "116")
    '''
    parameters = {
        'discipline': discipline, # F = 1 (ENG 116), F = 2 (CS 303)
        'keyword1': keyword1,
        'hocky': '70',
        't': '1599613145426'
    }

    r = requests.get('http://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx', parameters)
    soup = BeautifulSoup(r.text, 'html.parser')

    def XuLyUrlSub(url_sub: str) -> str:
        # http://courses.duytan.edu.vn/Sites/Home_ChuongTrinhDaoTao.aspx?p=home_listcoursedetail&courseid=55&timespan=70&t=s
        # http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid=55&semesterid=70&timespan=70
        url = "http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid=55&semesterid=70&timespan=70"
        courseid = url_sub[73:url_sub.find("×pan")]
        return url.replace(url[85:87], courseid)
    try:
        url_sub = soup.find_all(class_='hit')[2]['href']  # link sau khi press Search
        url_sub = XuLyUrlSub(url_sub)
        return url_sub
    except:
        return None

def Get_Soup(url_sub: str):
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup       

def GetName(soup):
    out = []
    tr_tags = soup.find_all('tr', class_="lop")
    for tr_tag in tr_tags:
        out.append(str(tr_tag.td.a.string).strip())
    return out

def GetID(soup): 
    list_sub_id = []

    templst = soup.find_all(class_="lop")
    for tr_tag in templst:
        temp = tr_tag.td.a
        td_tag = temp.parent
        next_td_tag = td_tag.findNext("td")
        list_sub_id.append(str(next_td_tag.text).strip())
    return list_sub_id

def GetSeat(soup):
    list_sub_seat = []
    templst = []
    td_list = soup.find_all("td", align = "center")
    for td_tag in td_list:
        templst.append((str(td_tag.text).strip()))
    for temp in templst:
        if (len(temp) <= 2) or temp == "Hết chỗ":
            list_sub_seat.append(temp)
    return list_sub_seat

def GetCredit(soup):
    '''
        Phương thức này trả về 1 int, không phải list vì Credit của các lớp bằng nhau
    '''
    templst = soup.find(style = "width: 130px;")
    for mem in templst:
        tr_tag = mem.parent
        tr_tag_next = tr_tag.findNext("tr")
        tinchi = str(tr_tag_next.text).strip()
    key = tinchi.find("(")
    tinchi = int(tinchi[key+1])
    return tinchi

def GetSchedule(soup):
    lst = []

    tr_list = soup.find_all("tr", class_='lop')
    for tr_tag in tr_list:
        lst.append(json.dumps(clean_SubTime(str(tr_tag('td')[6]))))
    return lst

def GetTeacher(soup):
    list_sub_teacher = []

    tr_list = soup.find_all("tr", class_='lop')
    for tr_tag in tr_list:
        list_sub_teacher.append(str(tr_tag('td')[9].text).strip())
    return list_sub_teacher

def GetPlace(soup):
    list_sub_place = []

    tr_list = soup.find_all("tr", class_='lop')
    for tr_tag in tr_list:
        list_sub_place.append(str(tr_tag('td')[8].text).strip())
    return list_sub_place

def GetWeekRange(soup):
    list_week = []

    td_list = soup.find_all("td", style = "text-align: center;")
    for td_tag in td_list:
        list_week.append(str(td_tag.text).strip())
    return list_week

def GetStatus(soup):
    lst = []

    tr_list = soup.find_all("tr", class_='lop')
    for tr_tag in tr_list:
        lst.append(str(tr_tag('td')[10].font.string))
    return lst

if __name__ == "__main__":
    url_sub = Get_Url("ENG", "116")
    print(GetSchedule(url_sub)[0])

