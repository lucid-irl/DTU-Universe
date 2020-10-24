import unittest
from Schedule import *


class TestCleanSchedules(unittest.TestCase):

    def setUp(self):
        self.Schedule = Schedule([{'T2':['07:00-09:00','07:00-10:15']},{'T5':['07:00-09:00']}])
        self.Schedule2 = Schedule([{'T3':['09:15-11:15']},{'T6':['09:15-11:15','07:00-10:15']}])

    def test_GetNumberLessionPerWeek(self):
        self.assertEqual(self.Schedule.getNumberLessonPerWeek(), 2)

    def test_GetDatesOfLesson(self):
        self.assertEqual(self.Schedule.getDatesOfLesson(), ["T2","T5"])
    
    def test_GetStudyTime1(self):
        self.assertEqual(self.Schedule.getStudyTime(), 315.0)
    
    def test_GetStudyTime2(self):
        self.assertEqual(self.Schedule2.getStudyTime(), 315.0)

    def test_GetTimeOfDate(self):
        self.assertEqual(self.Schedule.getTimeOfDate(Monday), ['07:00-09:00','07:00-10:15'])

    def test_GetTimeOfDate_2(self):
        self.assertEqual(self.Schedule.getTimeOfDate(Thursday), ['07:00-09:00'])

    def test_GetTimeOfDate_3(self):
        self.assertEqual(self.Schedule.getTimeOfDate(Sunday), [])

    def test_GetEndTimeOfDate(self):
        self.assertEqual(self.Schedule.getEndTimeOfDate(Thursday), ['09:00'])

        
if __name__ == "__main__":
    unittest.main()