<div align="center">
    <h1>Ứng dụng siêu cấp vũ trụ DTU</h1>
</div>

<div align="center" width=50px><img src="https://github.com/MrSometimeswinmid/DoAn/blob/main/Images/logo.png" /></div>

## Từ một ý tưởng đơn giản vãi loz
App này được hình thành từ một ý tưởng sơ khai nhất là lấy lịch học trên trang Course của DTU và lịch thi trên
phòng đào tạo DTU. Ứng dụng được viết bằng Python, giao diện được dựng trên PyQt5.
## Đến một cái đồ án với nhiều chức năng thật sự...vãi loz
Từ những ý tưởng sơ khai chúng tôi đã vẽ ra một loạt các chức năng râu ria khác. Nhưng ý tưởng chính vẫn là một
ứng dụng cho phép người dùng Xếp một bản xem trước của lịch học, phục vụ cho những kỳ đăng ký tín chỉ đầy chật vật
và đầy đau khổ. Những ý tưởng râu ria đằng sau như cho phép chèn lịch cá nhân, bờ la bờ la nhiều thứ khác.
## Bạn muốn phát triển một phiên bản khác
Dự án này được xây dựng trên Python 3.6.8 64-bit. Bạn cần PyQt5 và các thư viện liên quan nếu muốn phát triển dự án này thêm nữa.
File requirements.txt là cần thiết giúp bạn nhanh chóng cài thư viện và các công cụ cần thiết cho việc phát triển.
Mọi sự đóng góp đều được khuyến khích.
## Phần này để ghi nhận công lao của các bạn
Xin cảm ơn:
* [Trần Huy Hoàng](https://www.facebook.com/kietchay100) lớp Big Data.
* [Trần Tuấn Khôi](https://www.facebook.com/profile.php?id=100010060428020) lớp Big Data.
* [Nguyen Truong](https://www.facebook.com/truongbede.me/) lớp Big Data.
* [Trương A Xin](https://www.facebook.com/truongaxin/) lớp Chế biến code.

Bên trên là những thành viên sáng lập của Start-up Sống Vì Donate. Với các cột mốc quan trọng 14:30, 19:32, 21:59, căn phòng chừng 8 mét vuông và con mèo đen tên Tôm.
## Giấy phép
Tất cả file code trong kho này đều theo giấy phép MIT.
## Kiến trúc
### Kiến trúc bộ cào
Nói chung bộ cào sẽ xuất ra một file Excel có các cột như ID lớp, tên lớp,...Nhưng *quan trọng nhất vẫn là chuỗi Schedule*, chuỗi này quan trọng trong việc sắp xếp các môn trong một Tuần học. Hàm clean chuỗi này được mình viết chi tiết trong cleanSubTime.py

File excel lấy được sẽ trông như sau:
| ID               | Tên lớp       | Schedule  | Nơi học | Teacher | Số tín chỉ |
| ---------------- |:-------------:|:---------:|:-------:|:-------:|:----------:|
| ENG117202001009  | ENG 117 A     | [{"T2":["07:00-09:00","07:00-10:15"]},{"T5":["07:00-09:00"]}]   | Hoà Khánh Nam | NGUYỄN DŨNG | 3 |
| ENG117202001011  | ENG 117 AC    | [{"T2":["07:00-09:00","07:00-10:15"]},{"T5":["07:00-09:00"]}]   | Hoà Khánh Nam | VIẾT NIN    | 2 |
| ENG117202001012  | ENG 117 B     | [{"T2":["07:00-09:00"]},{"T5":["07:00-09:00"]}]                 | Hoà Khánh Nam | VĂN HIỀN    | 2 |
### Các class cốt lõi
### Schedule
Class này giúp bạn thao tác dễ dàng hơn với chuỗi Schedule có trong file excel. Nó bao gồm các phương thức tính toán thông kế đơn giản.
### Subject
Đây là class quan trọng đại diện cho một Môn học. Đóng vai trò quan trọng trong việc sắp xếp các môn lên lịch.
### Conflit
Class này như tên của nó, nó đại diện cho một xung đột giữa hai Schedule khi được thêm vào Semeter. Xung đột này được phát hiện thông
qua timedelta.
### Semeter
Class chính trong việc xử lý logic. Trung gian tương tác với GUI và Subjects.
