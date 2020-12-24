"""
CS4RSA Helpful Function
~~~~~~~~~~~~~~~~~
Module này chứa những hàm đơn giản phục vụ cho việc làm sạch dữ liệu, xử lý dữ liệu trong những context thường gặp như
làm sạch text sau khi lấy được từ một Tag trong BeautifulSoup, suy cụm data thành một nhóm data duy nhất.
"""

from typing import List


def toStringAndCleanSpace(text):
    """Trả về một chuỗi đã được làm sạch space ở hai bên."""
    return ' '.join(str(text).strip().split())

def clustering(listCondition: List, funcClustering, iter):
    """Hàm xử lý gom cụm dữ liệu.
    
    @listCondition: Là một list các callback có một tham số đầu vào là từng phần tử có trong iter.
    
    @funcClustering: Hàm này nhận vào một list các item có trong iter sau khi đã được lọc qua
    bằng các condition có trong listCondition.
    
    @iter: Là một list các item cần gom cụm."""
    clusters = []
    for conditionFunc in listCondition:
        listItemPass = list(filter(conditionFunc, iter))
        item = funcClustering(listItemPass)
        clusters.append(item)
    return clusters

if __name__ == "__main__":
    checkChan = lambda number: True if number%2==0 else False
    checkLe = lambda number: True if number%2==1 else False

    class group:

        def __init__(self, listNumber) -> None:
            self.listNumber = listNumber

        def __repr__(self) -> str:
            return '<group {0}>'.format(self.listNumber)

    def itemsToGroup(items):
        return group(items)

    items = [1,2,3,4,5,5,6,7,9,21,13,42,53,123,51]
    out = clustering([checkChan, checkLe], itemsToGroup, items)
    print(out)