import os
import sys
import webbrowser

from PyQt5.QtCore import QLine, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QTextDocument
from class_subject import Subject
from typing import List, Tuple

from bs4 import BeautifulSoup
from class_DTUWeb import DTULogin, DTUSession
from class_DTUCrawler import *
from class_homeCourseSearch import HomeCourseSearch

from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QStackedWidget, QWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt

from class_convertType import ConvertThisQObject
import team_config

class FindCurriculumId(DTUSession):
    """Tìm ra curriculumId."""
    PAGE = 'https://mydtu.duytan.edu.vn/sites/index.aspx?p=home_registeredall'

    def __init__(self, semesterId:str, yearId:str, ASPNETSessionIdDict: dict):
        super().__init__(ASPNETSessionIdDict)
        self.semesterId = semesterId
        self.yearId = yearId

    def getPageHomeRegisteredAll(self):
        params = {
            'semesterid':self.semesterId,
            'yearid':self.yearId
        }
        r = self.get(FindCurriculumId.PAGE, params=params)
        return r.text

    def getCurriculumId(self):
        page = self.getPageHomeRegisteredAll()
        soup = BeautifulSoup(page, 'lxml')
        inputTags = soup.find_all('input',class_ = 'btn-dangky btn-dangky-vn')
        onClickValue:str = inputTags[0]['onclick']
        return onClickValue.split(',')[4]

class ThreadCheckLogin(QThread):
    signal_canLogin = pyqtSignal(dict)
    signal_canNotLogin = pyqtSignal(bool)

    def __init__(self):
        QThread.__init__(self)
    
    def run(self):
        dtuLogin = DTULogin()
        cookies = dtuLogin.getCookiesFromChrome()
        sessionId = dtuLogin.getDTUSessionIDFromCookies(cookies)
        if dtuLogin.isCanLoginDTU(sessionId):
            self.signal_canLogin.emit(sessionId)
        else:
            self.signal_canNotLogin.emit(True)


class SubjectRegister(QDialog):
    signal_sessionId = pyqtSignal(dict)

    def __init__(self, classRegCodes: List[str], semesterId, yearId, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.semesterId = semesterId
        self.yearId = yearId
        self.classRegCodes = classRegCodes
        self.setupUI()

    def setupUI(self):
        uic.loadUi(team_config.UI_REGISTER,self)
        self.stackedWidget = ConvertThisQObject(self, QStackedWidget, 'stackedWidget').toQStackedWidget()
        self.stackedWidget.setCurrentIndex(0)
        # check chrome
        self.button_check_chrome_check = ConvertThisQObject(self, QPushButton, 'button_check_chrome_check').toQPushButton()
        self.button_check_chrome_ok = ConvertThisQObject(self, QPushButton, 'button_check_chrome_ok').toQPushButton()
        self.button_check_chrome_ok.clicked.connect(self.exitDialog)

        # install chrome
        self.label_not_found_chrome_image = ConvertThisQObject(self, QLabel, 'label_not_found_chrome_image').toQLabel()
        self.button_not_found_chrome_ok = ConvertThisQObject(self, QPushButton, 'button_not_found_chrome_ok').toQPushButton()
        self.button_not_found_chrome_ok.clicked.connect(self.exitDialog)
        self.button_not_found_chrome_install = ConvertThisQObject(self, QPushButton, 'button_not_found_chrome_install').toQPushButton()

        # check login
        self.button_check_session_id_check = ConvertThisQObject(self, QPushButton, 'button_check_session_id_check').toQPushButton()
        self.button_check_session_id_ok = ConvertThisQObject(self, QPushButton, 'button_check_session_id_ok').toQPushButton()
        self.button_check_session_id_ok.clicked.connect(self.exitDialog)
        self.label_check_session_id_image = ConvertThisQObject(self, QLabel, 'label_check_session_id_image').toQLabel()
        self.label_check_session_id_title = ConvertThisQObject(self, QLabel, 'label_check_session_id_title').toQLabel()

        # page_request_login
        self.button_request_login_login = ConvertThisQObject(self, QPushButton, 'button_request_login_login').toQPushButton()
        self.button_request_login_login.clicked.connect(self.openBrowserAtDTUHomePage)
        self.button_request_login_ok = ConvertThisQObject(self, QPushButton, 'button_request_login_ok').toQPushButton()
        self.button_request_login_ok.clicked.connect(self.exitDialog)
        self.label_request_login_image = ConvertThisQObject(self, QLabel, 'label_request_login_image').toQLabel()

        # page_captcha_typing
        self.button_captcha_next = ConvertThisQObject(self, QPushButton, 'button_captcha_next').toQPushButton()
        self.button_captcha_ok = ConvertThisQObject(self, QPushButton, 'button_captcha_ok').toQPushButton()
        self.button_captcha_ok.clicked.connect(self.exitDialog)
        self.label_captcha_image = ConvertThisQObject(self, QLabel, 'label_captcha_image').toQLabel()
        self.label_captcha_content = ConvertThisQObject(self, QLabel, 'label_captcha_content').toQLabel()
        self.lineEdit_captcha = ConvertThisQObject(self, QLineEdit, 'lineEdit_captcha').toQLineEdit()
        
        self.checkChrome()

    def checkChrome(self):
        """Kiểm tra Chrome đã cài đặt hay chưa."""
        chromeBrowsers = {
            'chrome64':'C:/Program Files/Google/Chrome/Application/chrome.exe',
            'chrome32':'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        }
        for name, path in chromeBrowsers.items():
            if os.path.exists(path):
                self.browserPath = path
                self.browserName = name
                self.button_check_chrome_check.setStyleSheet("""
                    QPushButton {
                        background-color: #2ecc71;
                        border-bottom: 5px solid #27ae60;
                    }
                    QPushButton:pressed {
                        border: none;
                    }
                """)
                self.button_check_chrome_check.setText('Tiếp tục')
                self.button_check_chrome_check.clicked.connect(self.checkLogin)
                return
        image = QPixmap('resources/check_chrome_1.png')
        self.label_not_found_chrome_image.setPixmap(image)
        self.button_not_found_chrome_install.clicked.connect(lambda: self.openBrowserAt('https://www.google.com/intl/vi_vn/chrome/'))
        self.stackedWidget.setCurrentIndex(1)

    def checkLogin(self):
        self.stackedWidget.setCurrentIndex(2)
        image = QPixmap('resources/check_session_id_1.png')
        self.label_check_session_id_image.setPixmap(image)
        self.threadCheckLogin = ThreadCheckLogin()
        self.threadCheckLogin.signal_canLogin.connect(self.slotCanLogin)
        self.threadCheckLogin.signal_canNotLogin.connect(self.changeFrameCheckLoginFail)
        self.threadCheckLogin.start()

    def slotCanLogin(self, sessionId):
        self.changeFrameCheckLoginSuccess(sessionId)
        self.signal_sessionId.emit(sessionId)

    def changeFrameCheckLoginSuccess(self, sessionId:str):
        self.button_check_session_id_check.setStyleSheet("""
                QPushButton {
                    background-color: #2ecc71;
                    border-bottom: 5px solid #27ae60;
                }
                QPushButton:pressed {
                    border: none;
                }
            """)
        image = QPixmap('resources\check_session_id_3.png')
        # add properties
        self.sessionId = sessionId
        self.dtuInfo = DTUInfoStudent(sessionId)
        self.studentName = self.dtuInfo.getUsername()
        self.studentId = self.dtuInfo.getStudentId()

        self.label_check_session_id_title.setText('Xin chào {0}'.format(self.studentName))
        self.label_check_session_id_image.setPixmap(image)
        self.button_check_session_id_check.setText('Tiếp tục')
        self.button_check_session_id_check.clicked.connect(self.typeCaptcha)

    def typeCaptcha(self):
        self.stackedWidget.setCurrentIndex(4)
        self.label_captcha_content.setTextFormat(Qt.RichText)
        self.label_captcha_content.setText("""
            <html>
            <head/>
                <body>
                    <p>
                        Đây là bước cuối cùng trước khi bạn nhấn Tiếp tục để thực hiện việc đăng ký tín chỉ tự động. 
                        Hãy làm chính xác những bước sau:
                    </p>
                    <p>
                        &gt; Đầu tiên hãy tới trang đăng ký tín chỉ nằm trong phần 
                        <span style=" font-style:italic;">Học tập &gt; Đăng ký môn học</span>.
                    </p>
                    <p>
                        &gt; Chọn đúng năm học và học kỳ rồi nhấn Tiếp tục.
                    </p>
                    <p>
                        &gt; Nhập mã captcha tại mục đăng ký như hình minh hoạ vào textbox bên dưới.
                    </p>
                    <p>
                        <br/>
                    </p>
                </body>
            </html>""")
        image = QPixmap('resources/register_captcha_image.png')
        self.label_captcha_image.setPixmap(image)
        self.label_captcha_image.setStyleSheet('border-radius: 0px; border: 1px solid red;')
        self.button_captcha_next.clicked.connect(self.register)


    def register(self):
        fc = FindCurriculumId(self.semesterId, self.yearId, self.sessionId)
        curriculumId = fc.getCurriculumId()
        captcha = self.lineEdit_captcha.text()
        print('captcha', captcha)
        print('subjects', self.classRegCodes)
        print('studentId', self.studentId)
        print('curriculumId', curriculumId)


    def changeFrameCheckLoginFail(self):
        self.stackedWidget.setCurrentIndex(3)
        image = QPixmap('resources/check_session_id_2.png')
        self.label_request_login_image.setPixmap(image)
        
    def openBrowserAtDTUHomePage(self):
        dtuHomePage = 'https://mydtu.duytan.edu.vn/Signin.aspx'
        webbrowser.register(self.browserName, None, webbrowser.BackgroundBrowser(self.browserPath))
        webbrowser.get(self.browserName).open(dtuHomePage)

    def openBrowserAt(self, url):
        webbrowser.open(url)


    def exitDialog(self):
        self.accept()

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.moving:
            self.move(event.globalPos()-self.offset)

if __name__ == "__main__":
    dtulogin = DTULogin()
    ck = dtulogin.getCookiesFromChrome()
    sid = dtulogin.getDTUSessionIDFromCookies(ck)

    # print(sid)

    # print(dtulogin.isCanLoginDTU(sid))

    hc = HomeCourseSearch()
    yearId = hc.getCurrentSchoolYearValue()
    semesterId = hc.getCurrentSemesterValue()

    fc = FindCurriculumId(semesterId, yearId, sid)
    curriculumId = fc.getCurriculumId()

    print(curriculumId)

    
    # subjects:Subject = []
    # studentId:str = ''
    # captcha:str = ''
    
    # app = QApplication(sys.argv)
    # w = QWidget()
    # w.show()
    # register = SubjectRegister('sid', 'subjects', 'studentId', 'curriculumId',w)
    # register.exec()
    # sys.exit(app.exec())


