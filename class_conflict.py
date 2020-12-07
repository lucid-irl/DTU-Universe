from datetime import time, timedelta
from time import sleep
from typing import List, Tuple
from unittest.signals import removeResult

from class_subject import *
from class_schedule import *

class Conflict:
    """Đại diện cho hai xung đột giữa hai Subject (bị chồng lịch học)."""

    def __init__(self, subject1: Subject, subject2: Subject):
        self.subject1 = subject1
        self.subject2 = subject2

    def __str__(self) -> str:
        return '<Conflict [{0}]--[{1}]>'.format(self.subject1.getName(), self.subject2.getName())
        
    def __repr__(self):
        return '<Conflict [{0}]--[{1}]>'.format(self.subject1.getName(), self.subject2.getName())

    def __eq__(self, o: object) -> bool:
        if ((self.subject1 == o.getSubject1() and self.subject2 == o.getSubject2()) or
            (self.subject1 == o.getSubject2() and self.subject2 == o.getSubject1())):
            return True
        else:
            return False

    def isConflict(self) -> bool:
        """**Không còn được dùng nữa**
        
        Kiểm tra xem hai Subject có xung đột về thời gian học hay không. Phương thức này sẽ tự động chạy
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

    def getGenericDate(self) -> Set[str]:
        """Trả về một set chứa những Thứ mà hai môn học nằm chung."""
        setday1 = set(self.subject1.getSchedule().getDatesOfLesson())
        setday2 = set(self.subject2.getSchedule().getDatesOfLesson())
        return setday1.intersection(setday2)

    def getConflictTime(self) -> List[Dict[str,Tuple[timedelta, timedelta]]]:
        """
        Trả về một List[Dict[Tuple]] chứa thời gian bắt đầu và thời gian kết thúc xung đột của hai môn học nào đó.
        [{Monday: ('07:00:00','8:00:00')}, {Tuseday: ('07:00:00','8:00:00')}]
        """
        output = []
        if self.subject1.getID() == self.subject2.getID():
            return output
        for day in self.getGenericDate():

            start1 = self.subject1.getSchedule().getStartTimeOfDate(day)
            end1 = self.subject1.getSchedule().getEndTimeOfDate(day)
            start2 = self.subject2.getSchedule().getStartTimeOfDate(day)
            end2 = self.subject2.getSchedule().getEndTimeOfDate(day)

            # Phân rã thành những cặp start và end
            timeRange1s = []
            for i in range(len(start1)):
                timeRange = [start1[i], end1[i]]
                timeRange1s.append(timeRange)

            timeRange2s = []
            for i in range(len(start2)):
                timeRange2 = [start2[i], end2[i]]
                timeRange2s.append(timeRange2)
        
            # So khớp từ cặp để tìm xung đột.
            for time_range_sub1 in timeRange1s:
                for time_range_sub2 in timeRange2s:
                    if (self.isThatRangeTimeInThisRangeTime(time_range_sub1, time_range_sub2)
                    or self.isThatRangeTimeInThisRangeTime(time_range_sub2, time_range_sub1)
                    or self.isTwoTimeRangeIntersect(time_range_sub1, time_range_sub2)
                    or self.isTwoTimeRangeIntersect(time_range_sub2, time_range_sub1)):
                        # sort lấy range giữa
                        time_ranges = time_range_sub1 + time_range_sub2
                        time_ranges = sorted(time_ranges)
                        output.append({day:(str(time_ranges[1]), str(time_ranges[2]))})
        return output

    def isInTimeRange(self, timeRange: List[timedelta], point: timedelta) -> bool:
        if point >= timeRange[0] and point <= timeRange[1]:
            return True
        else:
            return False
    
    def isThatRangeTimeInThisRangeTime(self, thatRangeTime: List[timedelta], thisRangeTime: List[timedelta]) -> bool:
        if self.isInTimeRange(thisRangeTime, thatRangeTime[0]) and self.isInTimeRange(thisRangeTime, thatRangeTime[1]):
            return True
        else:
            return False
    
    def isTwoTimeRangeIntersect(self, timeRange: List[timedelta], timeRange2: List[timedelta]):
        if self.isInTimeRange(timeRange, timeRange2[0]) and self.isInTimeRange(timeRange2, timeRange[1]):
            return True
        elif self.isInTimeRange(timeRange2, timeRange[0]) and self.isInTimeRange(timeRange, timeRange2[1]):
            return True
        else:
            return False

    def getSubject1(self):
        return self.subject1

    def getSubject2(self):
        return self.subject2

    def getInfo(self):
        return "Xung đột giữa hai môn {0} và {1}".format(self.subject1.getName(), self.subject2.getName())