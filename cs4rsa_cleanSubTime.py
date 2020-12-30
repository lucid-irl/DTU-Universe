import re
from typing import List
import re


def get_list_schedule_raw_from_html(html: str) -> List:
    """Trích xuất và lấy ra list schedule thô từ html."""
    schedules_raw = []
    join_schedules = []
    raw_sub_time = html.replace('\n','')
    strings = re.findall(r'>(.*?)<', raw_sub_time)
    for string in strings:
        row = str(string).strip().split()
        if row:
            schedules_raw.append(row)
    for item in schedules_raw:
        temp = ''.join(item)
        join_schedules.append(temp)
    return join_schedules


def cleanScheduleTime(raw_sub_time: str):
    """
    Hàm này nhận vào <td> element và trả về time có cấu trúc của Subject.
    Bộ datatest ở SubTimeTestHTML.
    """
    days = ["T2:","T3:","T4:","T5:","T6:","T7:","CN:"]
    join_schedules = get_list_schedule_raw_from_html(raw_sub_time)

    output = []
    anchor = 0
    index = 0
    while True:
        try:
            if bool(re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', join_schedules[index+1])) == False:
                break
        except:
            break
        if join_schedules[index] in days:
            anchor = index+1
            buoi_hoc = {} # output {'T2:': ['07:00-09:00', '07:00-10:15']}
            time_buoi_hoc = []
            while bool(re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', join_schedules[anchor])):
                time_buoi_hoc.append(join_schedules[anchor])
                anchor+=1
                if anchor == len(join_schedules):
                    break
            buoi_hoc[join_schedules[index][0:-1]] =  time_buoi_hoc
            index = anchor
            output.append(buoi_hoc)
    return output
