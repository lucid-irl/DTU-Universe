import sys
from bs4 import BeautifulSoup
import requests
import requests.utils
import thread_getSessionIdDTU
from PyQt5.QtWidgets import *
import logging


logging.basicConfig(level=logging.INFO)
class DTUInfoStudent:

    page_studyingwarning = 'https://mydtu.duytan.edu.vn/sites/index.aspx?p=home_studyingwarning&functionid=113'
    page_warningDetail = 'https://mydtu.duytan.edu.vn/Modules/mentor/WarningDetail.aspx?'

    def __init__(self, sessionId):
        self.session = requests.Session()
        requests.utils.add_dict_to_cookiejar(self.session.cookies, sessionId)

    def __getHTMLDtuPage(self, url, params=None):
        request = self.session.get(url, params=params)
        return request.text

    def getSpecialStudentID(self):
        html = self.__getHTMLDtuPage(self.page_studyingwarning)
        soup = BeautifulSoup(html, 'lxml')
        warningTable = soup.find(class_='tbresult')
        tdHaveSpecialID = warningTable('td')[2]
        onClickValue = tdHaveSpecialID.span['onclick']
        return str(onClickValue).split("'")[1]

    def getStudentInfo(self):
        specialStudentID = self.getSpecialStudentID()
        html = self.__getHTMLDtuPage(self.page_warningDetail, params={'stid':specialStudentID})
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



def getDTUHtmlPage(filename,sessionID, url):
    r = requests.get(url, cookies=sessionID)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(r.text))
    print('Done')

if __name__ == "__main__":
    # demo get thong tin sinh vien
    app = QApplication(sys.argv)
    thread = thread_getSessionIdDTU.ThreadGetSessionIdDTU()

    def getInfo(sessionID):
        dtu = DTUInfoStudent(sessionID)
        print(dtu.getStudentInfo())
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