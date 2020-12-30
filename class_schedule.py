"""
# Schedule module
~~~~~~~~~~~~~~~
## Class Schedule
Đại diện cho thời gian học của một môn trong một Tuần.

## Các Hằng thao tác liên quan
Ngoài ra sẽ có các Hằng về Thứ và Tuần giúp bạn dễ dàng hơn trong việc sử dụng:

MONDAY, TUSEDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY, WEEK
## Các Function liên quan
StringToSchedule() cho phép bạn chuyển chuỗi thời gian đã clean thành một Schedule.
Hàm này được viết nhằm mục đích nhanh chóng xử lý đống data time có trong file Excel
mà bạn đã lấy về được.
"""

from typing import List, Dict
import json
from datetime import timedelta


Monday = MONDAY = 'T2'
Tuseday = TUSEDAY = 'T3'
Wednesday = WEDNESDAY = 'T4'
Thursday = THURSDAY = 'T5'
Friday = FRIDAY = 'T6'
Saturday = SATURDAY = 'T7'
Sunday = SUNDAY = 'CN'

Week = WEEK = [Monday, Tuseday, Wednesday, Thursday, Friday, Saturday, Sunday]


class Schedule:
    """Đại diện cho thời gian biểu của một Subject trong một Tuần kéo dài cho đến hết giai đoạn."""

    def __init__(self, schedules: List[Dict[str, List]]) -> None:
        self.schedules = schedules

    def getNumberLessonPerWeek(self) -> int:
        """Trả về số buổi học mỗi tuần."""
        return len(self.schedules)

    def getDatesOfLesson(self) -> List[str]:
        """
        Trả về một list chứa Thứ học của môn đó trong tuần đó.

        >>> ["T2","T4","T6"]
        """
        output = []
        for lesson in self.schedules:
            for key in lesson.keys():
                output.append(key)
        return output

    def getStudyTime(self) -> int:
        """
        Trả về tổng phút lớn nhất có thể của môn học đó trong một Tuần.

        >>> s = Schedule([{'T2':['07:00-09:00','07:00-10:15']},{'T5':['07:00-09:00']}])
        >>> s.getStudyTime()
        >>> 315.0
        """
        time_sum = 0
        for lesson in self.schedules:
            for _, times in lesson.items():
                time_temp = 0
                for time in times:
                    delta_time = self.convertStringToTimeDelta(
                        time).total_seconds()
                    if delta_time > time_temp:
                        time_temp = delta_time
                time_sum += time_temp
        return time_sum/60

    def getTimeOfDate(self, day: str) -> List[str]:
        """
        Hàm này trả về một `List` chứa thời gian tương ứng với Thứ bạn truyền vào. Mặc định trả về một `List rỗng` nếu 
        Thứ truyền vào không có trong `Schedule`.
        """
        for lesson in self.schedules:
            for k, v in lesson.items():
                if k == day:
                    return v
        else:
            return []

    def getStartTimeOfDate(self, day: str, merge: bool = False) -> List[timedelta]:
        """Trả về một `List` chứa timedelta là thời gian `Bắt đầu` của buổi học trong một Thứ nào đó.

        >>> s = Schedule([{'T2':['07:00-09:00','07:00-10:15']},{'T5':['07:00-09:00']}])
        >>> s.getStartTimeOfDate(Monday)
        >>> ["07:00","07:00"]

        Như bạn có thấy thời gian `Bắt đầu` của một Subject trong một Thứ nào đó có thể trùng nhau. Nhưng nếu
        bạn cần gộp chúng lại, bạn chỉ cần set tham số merge thành `True`.

        Phương thức này trả về `[]` nếu Thứ không tìm thấy trong Schedule.
        """
        output = []
        time_of_date = self.getTimeOfDate(day)
        if time_of_date:
            for lesson in time_of_date:
                hour = int(lesson.split('-')[0].split(':')[0])
                minute = int(lesson.split('-')[0].split(':')[1])
                timedelta_output = timedelta(hours=hour, minutes=minute)
                output.append(timedelta_output)
        if merge:
            return [i for i in set(output)]
        return output

    def getEndTimeOfDate(self, day: str, merge: bool = False) -> List[timedelta]:
        """
        Trả về một `List` chứa timedelta là thời gian `Kết thúc` của buổi học trong một Thứ nào đó.

        Như bạn có thấy thời gian `Kết thúc` của một Subject trong một Thứ nào đó có thể trùng nhau. Nhưng nếu
        bạn cần gộp chúng lại, bạn chỉ cần set tham số merge thành `True`.

        Phương thức này trả về `List rỗng` nếu Thứ không tìm thấy trong Schedule.
        """
        output = []
        time_of_date = self.getTimeOfDate(day)
        if time_of_date:
            for lesson in time_of_date:
                hour = int(lesson.split('-')[1].split(':')[0])
                minute = int(lesson.split('-')[1].split(':')[1])
                timedelta_output = timedelta(hours=hour, minutes=minute)
                output.append(timedelta_output)
        if merge:
            return [i for i in set(output)]
        return output

    @staticmethod
    def convertStringToTimeDelta(pattern: str) -> timedelta:
        """
        Hàm nhận vào một `str` là chuỗi thời gian lấy từng buổi của môn học, trả về một timedelta
        đại diện cho khoảng thời gian của buổi học đó. Ta có thể dùng `total_seconds()` để lấy ra số giây chênh lệch.

        >>> s.convertStringToTimeDelta('07:00-09:00').total_seconds()
        >>> 7200.0
        """
        patterns = pattern.split('-')
        time1_hour = int(patterns[0].split(':')[0])
        time1_minute = int(patterns[0].split(':')[1])
        time2_hour = int(patterns[1].split(':')[0])
        time2_minute = int(patterns[1].split(':')[1])
        time1 = timedelta(hours=time1_hour, minutes=time1_minute)
        time2 = timedelta(hours=time2_hour, minutes=time2_minute)
        return time2 - time1


def StringToSchedule(raw: str) -> Schedule:
    """
    Hàm này nhận vào một string và trả về một Schedule.

    >>> s = StringToSchedule("[{"T2":["07:00-09:00","07:00-10:15"]},{"T5":["07:00-09:00"]}]")
    >>> s.getStudyTime()
    >>> 315.0
    """
    schedule_object = json.loads(raw)
    return Schedule(schedule_object)


if __name__ == "__main__":
    string = """[{"T2":["07:00-09:00","07:00-10:15"]},{"T5":["07:00-09:00"]}]"""
    s = StringToSchedule(string)
    print(s.getEndTimeOfDate(Thursday, merge=True))
