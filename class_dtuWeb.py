from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import browser_cookie3
import webbrowser
import os
import requests

class DTULogin:
    """Yêu cầu: Google Chrome được cài đặt trên máy tính."""

    def getCookiesFromChrome(self):
        """Trả về cookies của Google Chrome trong máy tính. Nếu Google Chrome chưa được cài đặt trong máy, trả về None."""
        try:
            return browser_cookie3.chrome()
        except:
            return None

    def isHomePageDTU(self, html: str) -> bool:
        """Kiểm tra HTML doc truyền vào có phải là trang chủ sau khi đăng nhập của MyDTU hay không."""
        soup = BeautifulSoup(html, 'lxml')
        nameStudent = soup.find(class_='hello man')
        if nameStudent:
            return True
        return False
    
    def isDTUCookiesTrue(self, cookies: CookieJar):
        """Trả về True nếu cookies truyền vào cho phép đăng nhập vào MyDTU.
        
        Lưu ý"""
        cookie = self.getDTUSessionIDFromCookies(cookies)
        if self.isCanLoginDTU(cookie):
            DTURequest = requests.get('https://mydtu.duytan.edu.vn/Sites/index.aspx?p=home_timetable&functionid=13', cookies=cookie)
            if self.isHomePageDTU(DTURequest.text):
                return True
            return False
        else:
            return False

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

    @staticmethod
    def getDTUSessionIDFromCookies(cookies: CookieJar):
        """Lấy ra sessionId từ Cookies."""
        for cookie in cookies:
            if cookie.name == 'ASP.NET_SessionId' and cookie.domain == 'mydtu.duytan.edu.vn':
                return {'ASP.NET_SessionId':cookie.value}
        return None

    @staticmethod
    def isCanLoginDTU(cookies: CookieJar):
        """Trả về True nếu có thể đăng nhập vào MyDTU, ngược lại trả về False.
        
        #### Phương thức này phụ thuộc hoàn toàn vào tình trạng máy chủ của MyDTU.
        Tất cả các lỗi trong lúc request đều sẽ khiến phương thức này trả về `False`."""

        try:
            DTURequest = requests.get('https://mydtu.duytan.edu.vn/Sites/index.aspx?p=home_timetable&functionid=13', cookies=cookies)
            if DTURequest.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def openAtDTU(self):
        """Mở trình duyệt tại trang đăng nhập của MyDTU."""
        browserName, browserPath = self.getBrowser()
        dtuHomePage = 'https://mydtu.duytan.edu.vn/Signin.aspx'
        webbrowser.register(browserName, None, webbrowser.BackgroundBrowser(browserPath))
        webbrowser.get(browserName).open(dtuHomePage)

    