from http.cookiejar import CookieJar
from typing import Dict
from bs4 import BeautifulSoup
from time import time


import browser_cookie3
import requests
import logging

def getTime() -> str:
    """Trả về số milisecond bắt đầu từ Unix Epoch bao gồm một chuỗi 13 chữ số nguyên."""
    return str(int(time()))

class DTULogin:
    """Yêu cầu: Google Chrome được cài đặt trên máy tính."""

    CHROME_HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}


    def getCookiesFromChrome(self):
        """Trả về cookies của Google Chrome trong máy tính. Nếu Google Chrome chưa được cài đặt trong máy, trả về None."""
        logging.info('Get cookies from Google Chrome')
        try:
            return browser_cookie3.chrome()
        except:
            return None

    @staticmethod
    def isHomePageDTU(html: str) -> bool:
        """Kiểm tra HTML doc truyền vào có phải là trang chủ sau khi đăng nhập của MyDTU hay không."""
        logging.info('Check html page is MyDTU home page is not.')
        soup = BeautifulSoup(html, 'lxml')
        nameStudent = soup.find(class_='hello man')
        if nameStudent:
            return True
        return False

    @staticmethod
    def getDTUSessionIDFromCookies(cookies: CookieJar):
        """Lấy ra ASPNETSessionIdDict từ Cookies."""
        logging.info('Get ASP.NET_SessionId from cookies')
        for cookie in cookies:
            if cookie.name == 'ASP.NET_SessionId' and cookie.domain == 'mydtu.duytan.edu.vn':
                return {'ASP.NET_SessionId':cookie.value}
        return {}

    def isCanLoginDTU(self, ASPNETSessionIdDict):
        """#### Phương thức này phụ thuộc hoàn toàn vào tình trạng máy chủ của MyDTU.
        Tham số:
        
        ASPNETSessionIdDict -- ASP.NET_SessionId của trang MyDTU.

        Trả về True nếu có thể đăng nhập vào MyDTU, ngược lại trả về False.
        Tất cả vấn đề về máy chủ, requests, ASPNETSessionIdDict đều khiến phương thức này trả về False."""
        logging.info('Check request, cookies, server')
        url = 'https://mydtu.duytan.edu.vn/Sites/index.aspx?p=home_timetable&functionid=13' 
        self.DTURequest = requests.get(url, cookies=ASPNETSessionIdDict, headers=self.CHROME_HEADER)
        
        if self.DTURequest.status_code == 200:
            if self.isHomePageDTU(self.DTURequest.text):
                return True
            return False
        else:
            return False

    def getName(self):
        """Trả về tên của Sinh viên nếu đăng nhập thành công."""
        soup = BeautifulSoup(self.DTURequest.text, 'lxml')
        nameStudent = soup.find(class_='hello man').text
        return nameStudent


class DTUSession:
    """Đảm nhận việc tạo Session và requests. Tham số truyền vào bắt buộc là ASP.NET_SessionId."""

    CHROME_HEADER = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }

    def __init__(self, ASPNETSessionIdDict: dict):
        self.dtuSession = requests.Session()
        self.cookies = ASPNETSessionIdDict
        self.dtuSession.headers = self.CHROME_HEADER

    def post(self, url, data=None, params=None):
        loggingString = 'POST request to {0}'.format(url)
        logging.info(loggingString)
        return self.dtuSession.post(url, data=data, params=params, cookies=self.cookies)

    def get(self, url, params=None):
        loggingString = 'GET request to {0}'.format(url)
        logging.info(loggingString)
        return self.dtuSession.get(url, params=params, cookies=self.cookies)



