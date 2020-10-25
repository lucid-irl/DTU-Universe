from bs4 import BeautifulSoup
import requests


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
        print('Không tìm thấy môn học {}'.format(discipline))

def GetName(url_sub: str): 
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')

    temp = soup.find_all(class_="nhom-lop")
    return [str(td_tag.div.string).strip() for td_tag in temp]

def GetID(url_sub: str): 
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    list_sub_id = []

    templst = soup.find_all(class_="lop")
    for tr_tag in templst:
        temp = tr_tag.td.a
        td_tag = temp.parent
        next_td_tag = td_tag.findNext("td")
        list_sub_id.append(str(next_td_tag.text).strip())
    for mem in list_sub_id:
        if mem == "":
            list_sub_id.remove(mem)
    return list_sub_id

def GetSeat(url_sub: str):
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')

    list_sub_seat = []
    templst = []
    td_list = soup.find_all("td", align = "center")
    for td_tag in td_list:
        templst.append((str(td_tag.text).strip()))
    for temp in templst:
        if (len(temp) <= 2) or temp == "Hết chỗ":
            list_sub_seat.append(temp)
    return list_sub_seat

def GetCredit(url_sub: str):
    '''
        Phương thức này trả về 1 int, không phải list vì Credit của các lớp bằng nhau
    '''
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')

    templst = soup.find(style = "width: 130px;")
    for mem in templst:
        tr_tag = mem.parent
        tr_tag_next = tr_tag.findNext("tr")
        tinchi = str(tr_tag_next.text).strip()
    key = tinchi.find("(")
    tinchi = int(tinchi[key+1])
    return tinchi

def GetSchedule(url_sub: str):
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    lst = []

    tr_list = soup.find_all("tr", class_='lop')
    index = 0
    print("tr 15:", tr_list[15])
    for tr_tag in tr_list:
        print('index:', index)
        print(clean_SubTime(str(tr_tag('td')[6])))
        index +=1

        

    return lst

def Get_TeacherAndPlace(url_sub: str):
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    list_sub_teacherandplace = []

    templst = soup.find_all(style = "text-align: center; vertical-align: top;")
    for temp in templst:
        td_tag = temp.next_sibling.next_sibling
        info = str(td_tag.text).strip()
        if info != "None":
            list_sub_teacherandplace.append(info)
    return list_sub_teacherandplace
    # Không lấy riêng teacher và place đc vì ở chung tag (xét chẵn lẻ)

def GetWeekRange(url_sub: str):
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    list_week = []

    td_list = soup.find_all("td", style = "text-align: center;")
    for td_tag in td_list:
        list_week.append(str(td_tag.text).strip())
    return list_week

def GetStatus(url_sub: str):
    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')
    list_status = []

    td_list = soup.find_all("td", align = "center", style = "width: 70px;")
    for td_tag in td_list:
        temp = td_tag[1]
        list_status.append(str(temp.text))
    return list_status
    # Trả về Tình trạng đăng ký và Tình trạng triển khai vì tag giống nhau (xét chẵn lẻ)

url_sub = Get_Url("ENG", "116")
print(url_sub)
print(GetStatus(url_sub))
