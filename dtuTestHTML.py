from bs4 import BeautifulSoup
from class_DTUCrawler import DTUSubjectSCore, DTUSemesterScore
import re

def major(f):
    soup = BeautifulSoup(f, 'lxml')
    ul = soup.find('ul',class_='tabNavigation')
    return str(ul.li.a.text).strip()


def isLoadAjaxBangDiem(tag):
    if re.search('(loadAjaxBangDiem\(\'[0-9]*\', \'[0-9]*\', \'[0-9]*\'\))', str(tag)) and tag.name == 'script':
        return True

def scores(f):
    soup = BeautifulSoup(f,'lxml')
    scriptLoadBangDiem = soup.find_all(isLoadAjaxBangDiem)
    listSemesterParams = []
    for tag in scriptLoadBangDiem:
        tag = ' '.join((str(tag).split()))
        functionLoadAjaxBangDiem = re.compile(r'>(.*?)<')
        group = functionLoadAjaxBangDiem.search(str(tag))
        listParams = str(group[1]).split("'")
        listSemesterParams.append([listParams[1],listParams[3], listParams[5]])
    print(listSemesterParams)

def crawlSubject(f):
    soup = BeautifulSoup(f, 'lxml')
    subjectScores = soup.find_all('tr', class_='diem')
    name = 'COM 101'
    if re.search('({})'.format(name),str(subjectScores[0].td.div.text).strip()):
        subjectScore = DTUSubjectSCore()
        subjectScore.maMon = str(subjectScores[0].td.div.text).strip()
        subjectScore.maLop = str(subjectScores[0]('td')[1].div.div.text).strip()
        subjectScore.hinhThuc = str(subjectScores[0]('td')[2].div.text).strip()
        subjectScore.tenMon = str(subjectScores[0]('td')[3].div.text).strip()
        subjectScore.soDonViHocTap = int(str(subjectScores[0]('td')[4].div.text).strip())
        subjectScore.loaiDonViHocTap = str(subjectScores[0]('td')[5].div.text).strip()
        subjectScore.diemGoc = float(str(subjectScores[0]('td')[6].div.text).strip())
        subjectScore.diemChu = str(subjectScores[0]('td')[7].div.text).strip()
        subjectScore.diemQuyDoi = float(str(subjectScores[0]('td')[8].div.text).strip())
        subjectScore.diemTichLuy = float(str(subjectScores[0]('td')[9].div.text).strip())
        # subjectScore.setData([maMon, maLop, hinhThuc, tenMon, soDonViHocTap, loaiDonViHocTap, diemGoc, diemChu, diemQuyDoi, diemTichLuy])
        print(subjectScore)
    else:
        print(None)

def summarys(f):
    soup = BeautifulSoup(f, 'lxml')
    summaryS = soup.find_all('tr', class_='footer')
    print(str(summaryS[0]('td')[1].div.text).strip)
    print('trung binh diem goc ky hoc', float(str(summaryS[1]('td')[1].text).strip()))



filename = 'html\\bangdiemhockychitiet.html'
with open(filename, 'r', encoding='utf-8') as f:
    summarys(f)
