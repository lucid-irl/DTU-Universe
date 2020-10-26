import unittest
from subject import *
from schedule import *
from conflict import Conflit

class TestConflict(unittest.TestCase):

    def setUp(self) -> None:
        self.sd1 = Schedule([{'T2':['07:00-09:00','07:00-10:15']},{'T5':['07:00-09:00']}])
        self.sd2 = Schedule([{'T2':['07:00-11:15']},{'T5':['07:00-09:00']}])
        self.s1 = Subject('1','ok',3,4,self.sd1,'ok','ok',(),True)
        self.s2 = Subject('1','ok',3,4,self.sd2,'ok','ok',(),True)
        self.cf = Conflit(self.s1, self.s2)

    def test_isConflict(self):
        self.assertEqual(self.cf.isConflict(), True)

    def test_getDateHaveConflict(self):
        self.assertEqual(self.cf.getDateHaveConflict(),['T2','T5'])

if __name__ == "__main__":
    unittest.main()