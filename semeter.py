from subject import Subject
from PyQt5.QtWidgets import QTableWidget
from schedule import *


class Semeter:
    SUBJECTS = [
        {"T2":[]},
        {"T3":[]},
        {"T4":[]},
        {"T5":[]},
        {"T6":[]},
        {"T7":[]},
        {"CN":[]}
    ]

    def __init__(self, table: QTableWidget) -> None:
        self.table = table

    def addSubjectToCalendar(self, subject: Subject):
        