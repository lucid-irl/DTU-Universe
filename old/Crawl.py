from bs4 import BeautifulSoup
import requests
import json

from cleanSubTime import cleanScheduleTime


def Get_Url(discipline: str, keyword1: str) -> str:
    '''
    Trả về đường link source của môn học
    >>> Get_Url("ENG", "116")
    '''
    parameters = {
        'discipline': discipline, # F = 1 (ENG 116), F = 2 (CS 303)
        'keyword1': keyword1,
        'hocky': '70',
    }

    r = requests.get('http://courses.duytan.edu.vn/Modules/academicprogram/CourseResultSearch.aspx', parameters)
    soup = BeautifulSoup(r.text, 'html.parser')

    def XuLyUrlSub(url_sub: str) -> str:
        print('url',url_sub)
        url = "http://courses.duytan.edu.vn/Modules/academicprogram/CourseClassResult.aspx?courseid=55&semesterid=70&timespan=70"
        courseid = url_sub[73:url_sub.find("×pan")]
        return url.replace(url[85:87], courseid)

    try:
        url_sub = soup.find_all(class_='hit')[2]['href']  # link sau khi press Search
        return XuLyUrlSub(url_sub)
    except:
        return None

def Get_Soup(url_sub: str):
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup       


def CheckExistLab(soup):
    '''
        Hàm này để kiểm tra môn học có lớp Thực hành không
        Nếu có sẽ trả về True, không có trả về False
    '''
    templst = []

    tr_tags = soup.find_all("tr", class_ = "lop")
    for tr_tag in tr_tags:
        templst.append(str(tr_tag('td')[2].string).strip())
    if len(set(templst)) == 2:
        return True
    else:
        return False

def GetListExistId(soup, lst_input: list):
    result = []
    key = []
    list_sub_id = []
    tr_tags = soup.find_all("tr", class_ = "lop")
    for tr_tag in tr_tags:
        list_sub_id.append(str(tr_tag('td')[1].a.string).strip())
    if CheckExistLab(soup):
        for i in range(len(list_sub_id)):
            if i % 2 == 0:
                list_sub_id[i] = list_sub_id[i+1]
    for i in range(len(list_sub_id)):
        if list_sub_id[i] != "":
            key.append(i)
    for i in range(len(lst_input)):
        if i in key:
            result.append(lst_input[i])
    return result

def GetName(soup):
    out = []
    tr_tags = soup.find_all('tr', class_="lop")
    for tr_tag in tr_tags:
        out.append(str(tr_tag.td.a.string).strip())
    return GetListExistId(soup, out)

def GetID(soup): 
    list_sub_id = []

    tr_tags = soup.find_all("tr", class_ = "lop")
    for tr_tag in tr_tags:
        list_sub_id.append(str(tr_tag('td')[1].a.string).strip())
    if CheckExistLab(soup):
        for i in range(len(list_sub_id)):
            if i % 2 == 0:
                list_sub_id[i] = list_sub_id[i+1]
    while ("" in list_sub_id):
        list_sub_id.remove("")
    return list_sub_id

def GetSeat(soup):
    list_sub_seat = []
    templst = []
    result = []
    td_list = soup.find_all("td", align = "center")
    for td_tag in td_list:
        templst.append((str(td_tag.text).strip()))
    for temp in templst:
        if (len(temp) <= 2) or temp == "Hết chỗ":
            list_sub_seat.append(temp)
    for mem in list_sub_seat:
        if mem == "Hết chỗ":
            result.append(int(0))
        else:
            result.append(int(mem))
    return GetListExistId(soup, result)

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
        lst.append(json.dumps(cleanScheduleTime(str(tr_tag('td')[6]))))
    return GetListExistId(soup, lst)

def GetWeekRange(soup):
    list_week = []

    td_list = soup.find_all("td", style = "text-align: center;")
    for td_tag in td_list:
        list_week.append(str(td_tag.text).strip())
    return GetListExistId(soup, list_week)

def GetStatus(soup):
    lst = []
    result = []
    tr_list = soup.find_all("tr", class_='lop')
    for tr_tag in tr_list:
        lst.append(str(tr_tag('td')[10].font.string))
    for mem in lst:
        if mem == "Còn Hạn Đăng Ký":
            result.append(int(1))
        else:
            result.append(int(0))
    return GetListExistId(soup, result)

def GetSubName(soup):
    div_tag = soup.find(class_ = "title-1")
    return div_tag.string[div_tag.string.find(":") + 1 : ].replace("  ", "").replace("\xa0\r\n", "")

def GetPlace(soup):
    list_sub_place = []
    result = []
    templst = [] 
    tr_list = soup.find_all("tr", class_='lop')
    for tr_tag in tr_list:
        list_sub_place.append(str(tr_tag('td')[8].text).split("\r\n"))

    for place in list_sub_place:
        for mem in place:
            temp = mem.strip()
            if temp != "":
                templst.append(temp)
        result.append(", ".join(templst))
        templst = []    

    return GetListExistId(soup, result)

def GetTeacher(soup):
    list_sub_teacher = []
    templst = []
    result = []

    tr_list = soup.find_all("tr", class_='lop')
    for tr_tag in tr_list:
        list_sub_teacher.append(str(tr_tag('td')[9].text).strip())
    for i in range(len(list_sub_teacher)):
        if list_sub_teacher[i] == "":
            list_sub_teacher[i] = "KHÔNG RÕ"
    for mem in list_sub_teacher:
        templst.append(mem.split())
    for temp in templst:
        result.append(" ".join(temp))

    return GetListExistId(soup, result)

if __name__ == "__main__":
    print(Get_Url("PSU-FIN","301"))