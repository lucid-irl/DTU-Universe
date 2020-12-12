from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import browser_cookie3
import webbrowser
import os
import requests
import logging


logging.basicConfig(level=logging.INFO)

CHROME_HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}


class DTULogin:
    """Yêu cầu: Google Chrome được cài đặt trên máy tính."""

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
        """Lấy ra sessionId từ Cookies."""
        logging.info('Get ASP.NET_SessionId from cookies')
        for cookie in cookies:
            if cookie.name == 'ASP.NET_SessionId' and cookie.domain == 'mydtu.duytan.edu.vn':
                return {'ASP.NET_SessionId':cookie.value}
        return None

    def isCanLoginDTU(self, sessionId):
        """#### Phương thức này phụ thuộc hoàn toàn vào tình trạng máy chủ của MyDTU.
        Tham số:
        
        sessionId -- ASP.NET_SessionId của trang MyDTU.

        Trả về True nếu có thể đăng nhập vào MyDTU, ngược lại trả về False.
        Tất cả vấn đề về máy chủ, requests, sessionId đều khiến phương thức này trả về False."""

        try:
            logging.info('Check request, cookies, server')
            DTURequest = requests.get(
                                    'https://mydtu.duytan.edu.vn/Sites/index.aspx?p=home_timetable&functionid=13', 
                                    cookies=sessionId,
                                    headers=CHROME_HEADER
                                    )
            if DTURequest.status_code == 200:
                if self.isHomePageDTU(DTURequest.text):
                    return True
                return False
            else:
                return False
        except:
            return False


class DTUSession:
    """Đảm nhận việc tạo Session và requests."""

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

    def __init__(self, cookies):
        CHROME_HEADER.update({'cookies':cookies})
        self.dtuSession = requests.Session()
        self.dtuSession.headers.update(CHROME_HEADER)

    def post(self, url, data=None, params=None):
        return self.dtuSession.post(url, data=data, params=params)

    def get(self, url, params=None):
        return self.dtuSession.get(url, params=params)


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