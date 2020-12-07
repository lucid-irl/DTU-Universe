from typing import List
from class_schedule import Schedule
import re


class ColorError(Exception):

    def __init__(self, color: str) -> None:
        self.color = color
        self.message = '{0} is Error :D'.format(self.color)
        super().__init__(message=self.message)

class Subject:
    """
    Đại diện cho một môn học trong một học kỳ có một ID nhất định.
    
    @info
    
    http://courses.duytan.edu.vn/Sites/Home_ChuongTrinhDaoTao.aspx?p=home_coursesearch

    @parameters

    `id`: Mã lớp học.

    `name`: Tên lớp học.

    `number_of_seats_left`: Số chỗ còn lại.

    `credits`: Số tín chỉ.

    `schedule`: Một Schedule object đại diện cho thời gian của môn đó trong một Tuần học.

    `teacher`: Tên giảng viên.

    `place`: Nơi học.

    `week_range`: Tuần học.

    `status`: Tình trạng đăng ký.

    `full_name`: Tên đầy đủ của môn học.
    """

    def __init__(self, id: str, name: str, number_of_seats_left: int, credits: int, schedule: Schedule, 
                teacher: str, place: str, week_range: list, status: int, full_name: str):
        self.id = id
        self.name = name
        self.full_name = full_name
        self.number_of_seats_left = number_of_seats_left  
        self.credits = credits
        self.schedule = schedule
        self.teacher = teacher
        self.place = place
        self.week_range = week_range
        self.status = status
        self.color = None

    def __str__(self):
        return "<Subject {0}>".format(self.name)

    def __repr__(self) -> str:
        return "<Subject {0}>".format(self.name)

    def __eq__(self, o: object) -> bool:
        if self.name == o.name:
            return True
        else:
            return False

    def getInfo(self):
        info = """Môn học: {0} | {5}\nHọc từ tuần {6} đến tuần {7}\nGiảng viên: {1} | Số tín chỉ: {2} | Số chỗ: {3}\nMôn này học tại {4}.""".format(self.name, self.teacher, self.credits, self.number_of_seats_left, self.place, self.full_name, self.week_range[0], self.week_range[1])
        return info

    def setColor(self, color: str):
        if re.match(r'^#(?:[0-9a-f]{3}){1,2}$', color):
            self.color = color
        else:
            raise ColorError(color)

    def getColor(self) -> str:
        return self.color

    def getSchedule(self) -> Schedule:
        return self.schedule

    def getName(self) -> str:
        return self.name
    
    def getStatus(self) -> int:
        return self.status

    def getID(self) -> str:
        return self.id

    def getFullName(self) -> str:
        return self.full_name

    def getWeekRange(self) -> List[int]:
        return [int(i) for i in self.week_range]