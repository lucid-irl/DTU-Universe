from bs4 import BeautifulSoup

filename = 'thongtinchitiet.html'

with open(filename, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')
    warningTable = soup.find('table')
    tdList = warningTable('td')
    username = tdList[1].strong.text
    studentID = tdList[4].text
    birthday = str(tdList[6].text).strip()
    cmnd = tdList[8].text
    dtuMail = tdList[10].a.text
    numberPhone = tdList[12].text
    location = tdList[15].text
    output = {
        'username':username,
        'studentID':studentID,
        'birthday':birthday,
        'cmnd':cmnd,
        'dtuMail':dtuMail,
        'numberPhone':numberPhone,
        'location':location
    }
    print(output)
    

