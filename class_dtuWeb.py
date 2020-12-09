import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import *


class DTULogin(QObject):

    signal_login_success = pyqtSignal('PyQt_PyObject')
    signal_login_fail = pyqtSignal('PyQt_PyObject')

    def __init__(self) -> None:
        super().__init__()
        import requests
        import browser_cookie3
        cj = browser_cookie3.chrome()
        for cookie in cj:
            if cookie.domain == 'mydtu.duytan.edu.vn' and cookie.name == 'ASP.NET_SessionId':
                cookie.value


if __name__ == "__main__":
    DTULogin()

