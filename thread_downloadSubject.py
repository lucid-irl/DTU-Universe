import time
from typing import List

from class_subjectCrawler import ExceptionCantFoundThisSubject, ExceptionNotHaveRegisterCode, ExceptionNotHaveSchedule, ExceptionSpecialSubject, SubjectData, SubjectPage
from PyQt5.QtCore import QThread, pyqtSignal


class ThreadShowLoading(QThread):
    """Hiệu ứng loading dễ thương 😃😃😃."""
    signal_changeTitle = pyqtSignal(str)
    signal_stopLoading = pyqtSignal(str)

    def __init__(self, timeRange: float, contents: List[str]):
        QThread.__init__(self)
        self.timeRange = timeRange
        self.contents = contents
        self.__isRunning = True

    def run(self):
        while self.__isRunning:
            for content in self.contents:
                self.signal_changeTitle.emit(content)
                time.sleep(self.timeRange)
        self.signal_stopLoading.emit(self.noti)

    def stopLoading(self,noti):
        self.noti = noti
        self.__isRunning=False

class ThreadDownloadSubject(QThread):

    signal_foundSubject = pyqtSignal('PyQt_PyObject')
    signal_notFoundSubject = pyqtSignal('PyQt_PyObject')
    signal_notHaveSchedule = pyqtSignal('PyQt_PyObject')
    signal_specialSubject = pyqtSignal('PyQt_PyObject')
    signal_subjectName = pyqtSignal(str)

    def __init__(self, semester: str, discipline: str, keyword1: str):
        QThread.__init__(self)
        self.semester = semester
        self.discipline = discipline
        self.keyword1 = keyword1
        self.subjectCode = discipline+' '+keyword1

    def run(self):
        try:
            try:
                subjectPage = SubjectPage(self.semester, self.discipline, self.keyword1)
                try:
                    subjectData = SubjectData(subjectPage)
                    self.signal_subjectName.emit(subjectPage.getName())
                    # subjects = subjectData.getSubjects()
                    self.signal_foundSubject.emit(subjectData)
                except ExceptionSpecialSubject:
                    self.signal_specialSubject.emit(subjectPage.getName())
            except ExceptionNotHaveSchedule:
                self.signal_notHaveSchedule.emit(self.subjectCode)
        except ExceptionCantFoundThisSubject:
            self.signal_notFoundSubject.emit(self.subjectCode)
