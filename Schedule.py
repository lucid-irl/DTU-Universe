from typing import List, Dict
import json
from datetime import timedelta


class Schedule:
    """
    Lịch học trong tuần của một môn
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Bao gồm các phương thức để lấy ra những thông tin cần thiết của tuần học đó.
    """

    def __init__(self, schedules: List[Dict[str,List]]) -> None:
        self.schedules = schedules

    def getNumberLessonPerWeek(self) -> int:
        """Trả về số buổi học mỗi tuần."""
        return len(self.schedules)

    def getDatesOfLesson(self) -> List[str]:
        """Trả về một list chứa Thứ học của môn đó trong tuần đó.
        
        >>> ["T2","T4","T6"]
        """
        output = []
        for lesson in self.schedules:
            for key in lesson.keys():
                output.append(key)
        return output

    def getStudyTime(self) -> int:
        """Trả về tổng phút lớn nhất có thể của môn học đó trong một Tuần.

        >>> s = Schedule([{'T2':['07:00-09:00','07:00-10:15']},{'T5':['07:00-09:00']}])
        >>> s.getStudyTime()
        >>> 315.0"""
        time_sum = 0
        for lesson in self.schedules:
            for _, times in lesson.items():
                time_temp = 0
                for time in times:
                    delta_time = self.convertStringToTimeDelta(time).total_seconds()
                    if delta_time > time_temp:
                        time_temp = delta_time
                time_sum += time_temp  
        return time_sum/60

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
        time1 = timedelta(hours=time1_hour,minutes=time1_minute)
        time2 = timedelta(hours=time2_hour, minutes=time2_minute)
        return time2 - time1

    
def StringToSchedule(raw: str) -> Schedule:
    """Hàm này nhận vào một string và trả về một Schedule.

    >>> s = StringToSchedule("[{"T2":["07:00-09:00","07:00-10:15"]},{"T5":["07:00-09:00"]}]")
    >>> s.getStudyTime()
    >>> 315.0"""
    object_ = json.loads(raw)
    return Schedule(object_)


if __name__ == "__main__":
    string = """[{"T2":["07:00-09:00","07:00-10:15"]},{"T5":["07:00-09:00"]}]"""
    s = StringToSchedule(string)
    # print(s.convertStringToTimeDelta('07:00-09:00').total_seconds())
    print(s.getStudyTime())