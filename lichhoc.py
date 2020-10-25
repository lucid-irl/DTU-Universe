from bs4 import BeautifulSoup
import requests
from xlwt import Workbook
import re
import pandas as pd
from PyQt5.QtCore import QThread

def Get_Url(discipline: str, keyword1: str) -> str:
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


#input
url_sub = Get_Url("CS", "401") 

def Get_Data(url_sub: str):
    # init list
    list_sub_name = []
    list_sub_id = []
    list_sub_date = []
    list_sub_time = []
    list_sub_place = []

    req = requests.get(url_sub)
    soup = BeautifulSoup(req.text, 'html.parser')

    # get sub name
    temp = soup.find_all(class_="nhom-lop")
    list_sub_name =  [str(td_tag.div.string).strip() for td_tag in temp]
    print(list_sub_name)

    # get sub ID
    templst = soup.find_all(class_="lop")
    for tr_tag in templst:
        temp = tr_tag.td.a
        td_tag = temp.parent
        next_td_tag = td_tag.findNext("td")
        list_sub_id.append(str(next_td_tag.text).strip())
    for mem in list_sub_id:
        if mem == "":
            list_sub_id.remove(mem)

    # get sub date
    templst = soup.find_all(style = "font-weight:normal; color:#4682B4;")
    for mem in templst:
        if mem.text != "":
            list_sub_date.append(str(mem.text).strip()[:2])
    
    # get sub time
    td_chua_gio_hoc = soup.find_all("tr", class_='lop')
    for lop in td_chua_gio_hoc:
        str_mem = str(lop("td")[6])
        new_mem = re.sub("<.*?>","",str_mem)
        new_mem = new_mem.strip().replace('\n',' ')
        print(new_mem)
        list_sub_time.append(new_mem)

    # get sub place and teacher
    templst = soup.find_all(style = "text-align: center; vertical-align: top;")
    for mem in templst:
        temp = mem.findNext("td")
        temp1 = temp.get_text()
        list_sub_place.append(str(temp1))

    result = [list_sub_id, list_sub_name,list_sub_date,list_sub_time,list_sub_place]
    return result

info = Get_Data(url_sub)

def init_excel(info: list):
    wb = Workbook()
    sheet1 = wb.add_sheet("sheet 1")

    # hàng trước cột sau :
    sheet1.write(0, 0, "STT")
    sheet1.write(0, 1, "Name")
    sheet1.write(0, 2, "ID")
    sheet1.write(0, 3, "Date")
    sheet1.write(0, 4, "Time")
    sheet1.write(0, 5, "Place")
    sheet1.write(0, 6, "Instructor")
    sheet1.write(0, 7, "Lec")
    sheet1.write(0, 8, "F")

    # dán dữ liệu trong info vào excel
    row = 1
    col = 0
    n = min(len(info[i]) for i in range(len(info)))
    for i in range(0, n):
        sheet1.write(row + i, col + 0, i + 1)
        sheet1.write(row + i, col + 1, info[0][i]) # name trong list la 0
        sheet1.write(row + i, col + 2, info[1][i]) # id
        sheet1.write(row + i, col + 3, info[3][i]) # date
        sheet1.write(row + i, col + 4, re.sub('[ ]+', ' ', info[4][i].rstrip().lstrip())) # time
        sheet1.write(row + i, col + 6, re.sub('([\n\r])', ' ', info[5][2 * i + 1].strip()))
        sheet1.write(row + i, col + 5, re.sub('([\n\r])', ' ', info[5][2 * i].strip())) # place
        sheet1.write(row + i, col + 7, info[6][i]) # Lec
        sheet1.write(row + i, col + 8, info[2][i]) # F

    wb.save("info.xls") 

init_excel(info)

def XuLyInput(str):
    return [str[:str.find(" ")], str[str.find(" ") + 1:]]