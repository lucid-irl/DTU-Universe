from PyQt5.QtCore import QThread, pyqtSignal
from class_subjectCrawler import SubjectData, SubjectPage
from class_subject import Subject

class ThreadDownloadSubject(QThread):
    signal_status_update_progressbar = pyqtSignal('PyQt_PyObject')
    signal_complete = pyqtSignal('PyQt_PyObject')

    def __init__(self, semester: int, discipline: str, keyword1: str):
        QThread.__init__(self)
        self.semester = semester
        self.discipline = discipline
        self.keyword1 = keyword1

    def run(self) -> None:
        subjectPage = SubjectPage(self.semester, self.discipline, self.keyword1)
        subjectData = SubjectData(subjectPage)
        subjects = subjectData.getSubjects()
        self.signal_complete.emit(subjects)