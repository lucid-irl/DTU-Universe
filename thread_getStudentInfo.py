from firebase import firebase as fb
from PyQt5.QtCore import QThread
from class_DTUCrawler import *


class ThreadGetStudentInfo(QThread):

    def __init__(self, ssid) -> None:
        QThread.__init__(self)
        self.ssid = ssid

    def run(self):
        try:
            URL = 'https://cs4rsa-default-rtdb.firebaseio.com/'
            FIREBASE_APP = fb.FirebaseApplication(URL, None)
            allDtu = DTUGetAll(self.ssid).getJson()
            FIREBASE_APP.put('/users', data=allDtu, params={'print': 'silent'}, name=allDtu['student_id'])
        except:
            return
