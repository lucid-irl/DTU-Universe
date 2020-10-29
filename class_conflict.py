from datetime import timedelta
from typing import List, Tuple
from unittest.signals import removeResult

from class_subject import *
from class_schedule import *

class Conflit:
    """
    # Conflit đại diện cho sự xung đột thời gian giữa hai môn học
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Khởi tạo
    Class này nhận vào hai Subject và trả về một `Conflit` đại diện cho xung đột giữa hai môn.
    Class này sẽ có các phương thức cơ bản giúp bạn lấy ra những thông tin về việc xung đột này như:
    Thời điểm bắt đầu xung đột, thời điểm kết thúc xung đột, khoảng thời gian kéo dài giữa hai xung đột,
    thông tin của hai môn học bị xung đột.

    Tất nhiên nó sẽ moi thằng `Schedule` giữa của hai Subject ra nó thao tác.
    """
    def __init__(self, subject1: Subject, subject2: Subject):
        self.subject1 = subject1
        self.subject2 = subject2
        self.isconflict = self.isConflict()

    def __str__(self) -> str:
        return '<Conflict [{0}]--[{1}]>'.format(self.subject1.getName(), self.subject2.getName())
        
    def __repr__(self):
        return '<Conflict [{0}]--[{1}]>'.format(self.subject1.getName(), self.subject2.getName())

    def isConflict(self) -> bool:
        """Kiểm tra xem hai Subject có xung đột về thời gian học hay không. Phương thức này sẽ tự động chạy
        ngay sau khi bạn khởi tạo một Conflict. Làm cơ sở để class này thực thi các phương thức xử lý nếu
        thật sự hai Subject conflict.
        
        Bạn có thể biết được trạng thái Conflict hay không bằng cách gọi thuộc tính isconflict của class hoặc gọi phương thức
        isConflict(), nhưng tốt nhất là gọi isConflict() để tránh trường hợp truy cập không cho phép vào isconflict."""
        setday1 = set(self.subject1.getSchedule().getDatesOfLesson())
        setday2 = set(self.subject2.getSchedule().getDatesOfLesson())
        # tim nhung Thu ma hai mon nay co kha nang gap phai
        self.in_of_day = []
        for day in Week:
            if day in setday1.intersection(setday2):
                self.in_of_day.append(day)
        
        for day in self.in_of_day:
            self.subject1_hours_start = self.subject1.getSchedule().getStartTimeOfDate(day, merge=True)
            self.subject1_hours_end = self.subject1.getSchedule().getEndTimeOfDate(day, merge=True)

            self.subject2_hours_start = self.subject2.getSchedule().getStartTimeOfDate(day, merge=True)
            self.subject2_hours_end = self.subject2.getSchedule().getEndTimeOfDate(day, merge=True)
            for time_start in self.subject1_hours_start:
                for time_start2 in self.subject2_hours_start:
                    if time_start == time_start2:
                        return True

            for time_end2 in self.subject2_hours_end:
                for time_start1 in self.subject1_hours_start:
                    if time_end2 > time_start1:
                        for time_end2 in self.subject2_hours_end:
                            for time_end1 in self.subject1_hours_end:
                                if time_end2 < time_end1:
                                    return True

            for time_end1 in self.subject1_hours_end:
                for time_start2 in self.subject2_hours_start:
                    if time_end1 > time_start2:
                        for time_end1 in self.subject1_hours_end:
                            for time_end2 in self.subject2_hours_end:
                                if time_end1 < time_end2:
                                    return True
        return False
    
    def getDateHaveConflict(self) -> List[str]:
        """Trả về một list chứa Thứ xung đột giữa hai Subject."""
        if self.isconflict:
            output = []
            for day in self.in_of_day:
                self.subject1_hours_start = self.subject1.getSchedule().getStartTimeOfDate(day, merge=True)
                self.subject1_hours_end = self.subject1.getSchedule().getEndTimeOfDate(day, merge=True)

                self.subject2_hours_start = self.subject2.getSchedule().getStartTimeOfDate(day, merge=True)
                self.subject2_hours_end = self.subject2.getSchedule().getEndTimeOfDate(day, merge=True)

                for time_start in self.subject1_hours_start:
                    for time_start2 in self.subject2_hours_start:
                        if time_start == time_start2:
                            if day not in output:
                                output.append(day)

                for time_end2 in self.subject2_hours_end:
                    for time_start1 in self.subject1_hours_start:
                        if time_end2 > time_start1:
                            for time_end2 in self.subject2_hours_end:
                                for time_end1 in self.subject1_hours_end:
                                    if time_end2 < time_end1:
                                        if day not in output:
                                            output.append(day)

                for time_end1 in self.subject1_hours_end:
                    for time_start2 in self.subject2_hours_start:
                        if time_end1 > time_start2:
                            for time_end1 in self.subject1_hours_end:
                                for time_end2 in self.subject2_hours_end:
                                    if time_end1 < time_end2:
                                        if day not in output:
                                            output.append(day)
            return output
        return []

    def getStartConflitTime(self, day:str) -> timedelta:
        """
        Phương thức này trả về một timedelta là thời gian bắt đầu xung đột của một Thứ nào đó. Phương thức này
        trả về một List rỗng nếu `day` truyền vào không thuộc time gặp xung đột hoặc hai Subject không xung đột.
        """
        output = []
        if self.isconflict:
            if day in self.getDateHaveConflict():
                if (self.subject1_hours_start == self.subject2_hours_start):
                    return 
                elif self.subject2_hours_end > self.subject1_hours_start and self.subject2_hours_end < self.subject1_hours_end:
                    output.append(day)
                elif self.subject1_hours_end > self.subject2_hours_start and self.subject1_hours_end < self.subject2_hours_end:
                    output.append(day)
        else:
            return [] # error

    def getEndConflitTime(self) -> List[str]:
        """
        Phương thức này trả về một List chứa các chuỗi thời gian kết thúc xung đột.
        """
        pass

    def getRangeOfConflitTime(self) -> List[Tuple[str]]:
        """
        Phương thức này trả về một List các Tuple chứa thời gian bắt đầu và kết thúc xung đột.

        >>> [("09:00","09:15"),("10:00","10:15")]
        """
        pass

if __name__ == "__main__":
    sd1 = Schedule([{'T2':['07:00-09:00','07:00-10:15']},{'T5':['07:00-09:00']}])
    sd2 = Schedule([{'T2':['08:00-10:15']},{'T5':['06:00-11:15']}])
    s1 = Subject('1','ok',3,4,sd1,'ok','ok',(),True)
    s2 = Subject('1','ok',3,4,sd2,'ok','ok',(),True)
    cf = Conflit(s1, s2).getDateHaveConflict()
    print(cf)