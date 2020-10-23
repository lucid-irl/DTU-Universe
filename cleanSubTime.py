# Triển khai tất cả các hàm dùng để làm sạch data ở đây
# Hàm phải luôn nhận vào dữ liệu thô và trả về dữ liệu đã được clean dưới dạng string hoặc
# các dạng có cấu trúc như list hoặc dict dễ dàng cho việc thao tác và truy xuất.

# Hàm làm sạch luôn có tên bắt đầu bằng clean_<name define>

import re
import SubTimeTestHTML.markup1
import SubTimeTestHTML.markup2
import SubTimeTestHTML.markup3
import SubTimeTestHTML.markup4
import re

def clean_SubTime(raw_sub_time: str):
    """Hàm này nhận vào <td> element và trả về time có cấu trúc của Subject.
    Bộ datatest ở SubTimeTestHTML.
    """
    day = ["T2:","T3:","T4:","T5:","T6:","T7:","CN:"]
    schedules = []
    join_schedules = []
    raw_sub_time = raw_sub_time.replace('\n','')
    strings = re.findall(r'>(.*?)<', raw_sub_time)
    for string in strings:
        row = str(string).strip().split()
        if row:
            schedules.append(row)

    for item in schedules:
        temp = ''.join(item)
        join_schedules.append(temp)
    output = []
    anchor = 0
    index = 0
    while True:
        if bool(re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', join_schedules[index+1])) == False:
            break
        if join_schedules[index] in day:
            anchor = index+1
            buoi_hoc = {} # output {'T2:': ['07:00-09:00', '07:00-10:15']}
            time_buoi_hoc = []
            while bool(re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', join_schedules[anchor])):
                time_buoi_hoc.append(join_schedules[anchor])
                anchor+=1
            buoi_hoc[join_schedules[index][0:-1]] =  time_buoi_hoc
            index = anchor
            output.append(buoi_hoc)
    return output
        
if __name__ == "__main__":
    print(clean_SubTime(SubTimeTestHTML.markup4.markup))

