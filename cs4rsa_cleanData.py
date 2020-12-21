"""
CS4RSA Clean Data
~~~~~~~~~~~~~~~~~
Module này chứa những hàm đơn giản phục vụ cho việc làm sạch dữ liệu trong những context thường gặp như
làm sạch text sau khi lấy được từ một Tag trong BeautifulSoup.
@ Mọi hàm làm sạch dữ liệu sẽ đều được đặt ở đây.
"""

def toStringAndCleanSpace(text):
    """Trả về một chuỗi đã được làm sạch space ở hai bên."""
    return str(text).strip()