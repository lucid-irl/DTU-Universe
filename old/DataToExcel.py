from xlwt import Workbook
from Crawl import *
from os import path

import os
import team_config


def CreateFolderToSave():
    if path.exists(team_config.FOLDER_SAVE_EXCEL) == False:
        os.mkdir(team_config.FOLDER_SAVE_EXCEL)

def CreateExcel(name: str, number: str) -> bool:
    excel_name = name + " " + number + '.xls'
    
    wb = Workbook()
    sheet1 = wb.add_sheet("sheet 1")
    try:
        soup = Get_Soup(Get_Url(name, number))
    except:
        return False

    sheet1.write(0, 0, "STT")
    sheet1.write(0, 1, "ID")
    sheet1.write(0, 2, "Name")
    sheet1.write(0, 3, "Schedule")
    sheet1.write(0, 4, "Place")
    sheet1.write(0, 5, "Teacher")
    sheet1.write(0, 6, "Credit")
    sheet1.write(0, 7, "Seat Left")
    sheet1.write(0, 8, "Week Range")
    sheet1.write(0, 9, "Status")
    sheet1.write(0, 10, "Subject Name")

    url_sub = Get_Url(name, number)
    soup = Get_Soup(url_sub)
    n = len(GetName(soup))
    row = 1
    col = 0

    for i in range(n):
        sheet1.write(row + i, col, str(i + 1))
        sheet1.write(row + i, col + 1, GetID(soup)[i])
        sheet1.write(row + i, col + 2, GetName(soup)[i])
        sheet1.write(row + i, col + 3, GetSchedule(soup)[i])
        sheet1.write(row + i, col + 4, GetPlace(soup)[i])
        sheet1.write(row + i, col + 5, GetTeacher(soup)[i])
        sheet1.write(row + i, col + 6, GetCredit(soup))
        sheet1.write(row + i, col + 7, GetSeat(soup)[i])
        sheet1.write(row + i, col + 8, GetWeekRange(soup)[i])
        sheet1.write(row + i, col + 9, GetStatus(soup)[i])
        sheet1.write(row + i, col + 10, GetSubName(soup))
    
    CreateFolderToSave()
    wb.save(team_config.FOLDER_SAVE_EXCEL+"/"+ excel_name)
    return True