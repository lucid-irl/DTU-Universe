# testing ở đây
# một phần mềm sẽ chả là một phần mềm nếu không có test

import unittest
from unittest.main import main
from cleanSubTime import clean_SubTime
import SubTimeTestHTML.markup1
import SubTimeTestHTML.markup2
import SubTimeTestHTML.markup3
import SubTimeTestHTML.markup4

class TestCleanMarkup(unittest.TestCase):

    def test_cleanMarkup1(self):
        self.assertEqual(clean_SubTime(SubTimeTestHTML.markup1.markup), [{'T3:':['09:15-11:15']},{'T6:':['09:15-11:15','07:00-10:15']}])

    def test_cleanMarkup2(self):
        self.assertEqual(clean_SubTime(SubTimeTestHTML.markup2.markup), [{'T2:':['15:15-17:15']},{'T5:':['15:15-17:15']}])

    def test_cleanMarkup3(self):
        self.assertEqual(clean_SubTime(SubTimeTestHTML.markup3.markup), [{'T2:':['07:00-09:00','07:00-10:15']},{'T5:':['07:00-09:00']}])

    def test_cleanMarkup4(self):
        self.assertEqual(clean_SubTime(SubTimeTestHTML.markup4.markup), [{'T7:':['17:45-21:00']}])

if __name__ == "__main__":
    unittest.main()