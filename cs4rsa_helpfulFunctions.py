"""
CS4RSA Helpful Function
~~~~~~~~~~~~~~~~~
Module này chứa những hàm đơn giản phục vụ cho việc làm sạch dữ liệu, xử lý dữ liệu trong những context thường gặp như
làm sạch text sau khi lấy được từ một Tag trong BeautifulSoup, suy cụm data thành một nhóm data duy nhất.
"""

import re
from typing import Dict, List


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

def getListStringMatchRegex(string: str, regexString:str):
    regex = re.compile(regexString)
    return [item for item in regex.findall(string) if item]

def getListObjectFromIndex(listIndex, listObject):
    """Lấy ra một list các object dựa theo list index được truyền vào."""
    output = []
    for i in listIndex:
        output.append(listObject[i])
    return output

def getNewListWithoutIndex(listIndex, listObject):
    """Lấy ra danh sách các object trong một list các object mà chúng không thuộc list index được truyền vào."""
    output = []
    for i in range(len(listObject)):
        if i in listIndex:
            continue
        output.append(listObject[i])
    return output

def getIndexOfKeyInDict(d:Dict, k: str):
    index = 0
    for key, _ in d.items():
        if key == k:
            return index
        index += 1
    return None

def getColFromMatrix(matrix: List[List[str]], colIndex: int) -> List[str]:
    if colIndex >= len(matrix[0]):
        return []
    output = []
    for row in matrix:
        output.append(row[colIndex])
    return output


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
