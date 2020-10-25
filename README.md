# Ứng dụng siêu cấp vũ trụ DTU

## Từ một ý tưởng đơn giản vãi loz
App này được hình thành từ một ý tưởng sơ khai nhất là lấy lịch học trên trang Course của DTU và lịch thi trên
phòng đào tạo DTU. Ứng dụng được viết bằng Python, giao diện được dựng trên PyQt5.
## Đến một cái đồ án với nhiều chức năng thật sự...vãi loz
Từ những ý tưởng sơ khai chúng tôi đã vẽ ra một loạt các chức năng râu ria khác. Nhưng ý tưởng chính vẫn là một
ứng dụng cho phép người dùng Xếp một bản xem trước của lịch học, phục vụ cho những kỳ đăng ký tín chỉ đầy chật vật
và đầy đau khổ. Những ý tưởng râu ria đằng sau như cho phép chèn lịch cá nhân, bờ la bờ la nhiều thứ khác.

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
Class này là class chính thao tác với TableWidget đảm nhiệm việc gắn Subject lên Table, sinh ra các signal quan trọng khi có xung đột.
#### * Thêm Subject
Semeter có một phương thức addSubjectToCalendar() thêm Subject, nó sẽ thêm Subject vào một List. Sau đó, nó sẽ tự động chạy phương thức scanConflit() - Phương thức này trả về một List chứa các Conflix object. Cuối cùng Semeter sẽ chạy hàm show() để hiển thị lịch
lên table dựa theo list Subject cùng với đó là vẽ xung đột thời gian cuối cùng.
#### * Xoá Subject
Thao tác xoá đơn giản là xoá Subject cho ID chỉ định ra khỏi Semeter và gọi lại phương thức show() của Semeter để vẽ lại lịch.
