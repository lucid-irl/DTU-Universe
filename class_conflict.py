from datetime import timedelta
from typing import List, Set, Tuple

from class_subject import *
from class_schedule import *

class Conflict:
    """Đại diện cho hai xung đột giữa hai Subject (bị chồng lịch học)."""

    def __init__(self, subject1: Subject, subject2: Subject):
        self.subject1 = subject1
        self.subject2 = subject2

    def __str__(self) -> str:
        return '<Conflict [{0}]--[{1}]>'.format(self.subject1.getSubjectCode(), self.subject2.getSubjectCode())
        
    def __repr__(self):
        return '<Conflict [{0}]--[{1}]>'.format(self.subject1.getSubjectCode(), self.subject2.getSubjectCode())

    def __eq__(self, o: object) -> bool:
        if ((self.subject1 == o.getSubject1() and self.subject2 == o.getSubject2()) or
            (self.subject1 == o.getSubject2() and self.subject2 == o.getSubject1())):
            return True
        else:
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

        Sẽ trả về một List rỗng khi:
        - Hai Subject có cùng mã đăng ký.
        - Hai Subject không xung đột tuần học.
        """
        output = []
        if isIntersectWeek(self.subject1, self.subject2):
            logging.info('IsisIntersectWeek True')
            if self.subject1.getSubjectCode() == self.subject2.getSubjectCode():
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
