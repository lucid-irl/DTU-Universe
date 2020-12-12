from class_DTUWeb import *
from typing import Dict
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *

import requests
import requests.utils
import thread_getSessionIdDTU
import logging
import sys

logging.basicConfig(level=logging.INFO)
class DTUInfoStudent:
    """Class này chịu trách nhiệm lấy thông tin của sinh viên DTU."""

    CHROME_HEADER = {
        ':authority': 'mydtu.duytan.edu.vn',
        ':method': 'POST',
        ':scheme': 'https',
        'accept': 'text/html, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'content-length': '7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://mydtu.duytan.edu.vn',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    page_studyingwarning = 'https://mydtu.duytan.edu.vn/sites/index.aspx?p=home_studyingwarning&functionid=113'
    page_warningDetail = 'https://mydtu.duytan.edu.vn/Modules/mentor/WarningDetail.aspx?'
    page_loadChuongTrinhHoc = 'https://mydtu.duytan.edu.vn/Modules/curriculuminportal/ajax/LoadChuongTrinhHoc.aspx?'

    def __init__(self, sessionId):
        """Khởi tạo một Session cho phép đăng nhập vào DTU thông qua sessionId.
        Sau khi đăng nhập xong, tự động chạy phương thức `getSpecialStudentID()` lấy
        specialNumber."""
        logging.info('init session and get special id')
        self.session = requests.Session()
        self.session.headers.update(CHROME_HEADER)
        requests.utils.add_dict_to_cookiejar(self.session.cookies, sessionId)
        self.specialNumber = self.getSpecialStudentID()

    def __getRequestToMyDTU(self, url, params=None):
        """Gởi một GET request tới MyDTU đi kèm params là các tham số được truyền vào dưới dạng một dict.
        Trả về HTML Page"""
        logging.info('send get request to {0}'.format(url))
        request = self.session.get(url, params=params)
        return request.text

    def __postRequestToMyDTU(self, url, params=None):
        """Gởi một POST request tới MyDTU đi kèm params là các tham số được truyền vào dưới dạng một dict.
        Trả về HTML Page"""
        logging.info('send post request to {0}'.format(url))
        request = self.session.post(url, params=params)
        return request.text  

    def getSpecialStudentID(self):
        """Trả về chuỗi đặc biệt được hash bởi một phương thức đặc biệt từ mã sinh viên."""
        logging.info('get special id')
        html = self.__getRequestToMyDTU(self.page_studyingwarning)
        soup = BeautifulSoup(html, 'lxml')
        warningTable = soup.find(class_='tbresult')
        tdHaveSpecialID = warningTable('td')[2]
        onClickValue = tdHaveSpecialID.span['onclick']
        return str(onClickValue).split("'")[1]

    def getStudentInfo(self) -> Dict:
        """Trả về một dict chứa thông tin cơ bản của sinh viên."""
        logging.info('get student infomation')
        specialStudentID = self.getSpecialStudentID()
        html = self.__getRequestToMyDTU(self.page_warningDetail, params={'stid':specialStudentID})
        soup = BeautifulSoup(html, 'lxml')
        warningTable = soup.find('table')
        tdList = warningTable('td')
        username = tdList[1].strong.text
        studentID = tdList[4].text
        birthday = str(tdList[6].text).strip()
        cmnd = tdList[8].text
        dtuMail = tdList[10].a.text
        numberPhone = tdList[12].text
        location = tdList[15].text
        output = {
            'username':username,
            'studentID':studentID,
            'birthday':birthday,
            'cmnd':cmnd,
            'dtuMail':dtuMail,
            'numberPhone':numberPhone,
            'location':location
        }
        return output

    def getMajor(self) -> Dict:
        """Trả về một dict là ngành học của sinh viên."""
        logging.info('get major')
        html = self.__postRequestToMyDTU(self.page_loadChuongTrinhHoc, {'studentidnumber':self.specialNumber})
        soup = BeautifulSoup(html,'lxml')
        ul = soup.find('ul',class_='tabNavigation')
        return str(ul.li.a.text).strip()


    @staticmethod
    def toHTMLFile(filename: str, html: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(html))



if __name__ == "__main__":
    # demo get thong tin sinh vien
    app = QApplication(sys.argv)
    thread = thread_getSessionIdDTU.ThreadGetSessionIdDTU()

    def getInfo(sessionID):
        dtu = DTUInfoStudent(sessionID)
        print(dtu.getMajor())
        app.exit()

    def close(mess):
        print(mess)
        app.exit(1)

    thread.signal_havedSessionId.connect(getInfo)
    thread.signal_somethingError.connect(lambda: close('gap van de ve may chu hoac cookie'))
    thread.signal_requestLogin.connect(lambda: close('yeu cau dang nhap'))
    thread.signal_chromeIsNotFound.connect(lambda: close('yeu cau cai dat Chrome'))
    thread.start()

    app.exec()

    # get html page
    # DTUSession()
    # url = 'https://mydtu.duytan.edu.vn/Modules/curriculuminportal/ajax/LoadChuongTrinhHoc.aspx?t=1607769858920&studentidnumber=ppxdPtQCkOX2+rc5tqBFhg%3D%3D'
    # specialNumber = 'ppxdPtQCkOX2+rc5tqBFhg%3D%3D'
    # postDTUHtmlPage('chuongtrinhhoc.html',{'ASP.NET_SessionId':'lwgrbs4wyskvybtm44jaszw5'},url,{'studentidnumber':specialNumber})