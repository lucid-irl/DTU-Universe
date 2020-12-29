from http.cookiejar import CookieJar
from typing import Dict
from bs4 import BeautifulSoup
from firebase import firebase
from time import time

import browser_cookie3
import webbrowser
import os
import requests
import logging


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
        return None

    def isCanLoginDTU(self, ASPNETSessionIdDict):
        """#### Phương thức này phụ thuộc hoàn toàn vào tình trạng máy chủ của MyDTU.
        Tham số:
        
        ASPNETSessionIdDict -- ASP.NET_SessionId của trang MyDTU.

        Trả về True nếu có thể đăng nhập vào MyDTU, ngược lại trả về False.
        Tất cả vấn đề về máy chủ, requests, ASPNETSessionIdDict đều khiến phương thức này trả về False."""
        try:
            logging.info('Check request, cookies, server')
            url = 'https://mydtu.duytan.edu.vn/Sites/index.aspx?p=home_timetable&functionid=13', 
            DTURequest = requests.get(url, cookies=ASPNETSessionIdDict, headers=self.CHROME_HEADER)
            if DTURequest.status_code == 200:
                if self.isHomePageDTU(DTURequest.text):
                    return True
                return False
            else:
                return False
        except:
            return False


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

    @staticmethod
    def getTime() -> str:
        """Trả về số milisecond bắt đầu từ Unix Epoch bao gồm một chuỗi 13 chữ số nguyên."""
        return str(int(time()))


class OpenBrowser:

    def openAtDTU(self):
        """Mở trình duyệt tại trang đăng nhập của MyDTU."""
        browserName, browserPath = self.getBrowser()
        dtuHomePage = 'https://mydtu.duytan.edu.vn/Signin.aspx'
        webbrowser.register(browserName, None, webbrowser.BackgroundBrowser(browserPath))
        webbrowser.get(browserName).open(dtuHomePage)

    @staticmethod
    def getBrowser():
        """Trả về đường dẫn Chrome được cài đặt trên thiết bị này."""
        browserPath = ''
        browserName = ''
        chromeBrowsers = {
            'chrome64':'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'chrome32':'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        }
        for name, path in chromeBrowsers:
            if os.path.exists(path):
                browserPath = path
                browserName = name
                return browserName, browserPath
        else:
            return None


class DTUFirebase:

    URL = 'https://cs4rsa-default-rtdb.firebaseio.com/'
    FIREBASE_APP = firebase.FirebaseApplication(URL, None)

    def appendStudentData(self, studentData):
        try:
            self.FIREBASE_APP.put('/users', data=studentData, params={'print': 'silent'}, name=studentData['student_id'])
        except:
            print(':)')

