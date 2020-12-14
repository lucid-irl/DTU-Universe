from bs4.element import ResultSet
from class_DTUWeb import *
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *

import requests
import requests.utils
import thread_getSessionIdDTU
import logging
import sys
import base64
import re

logging.basicConfig(level=logging.INFO)

class DTUInfoStudent:
    """Class này chịu trách nhiệm lấy thông tin của sinh viên DTU."""

    CHROME_HEADER = {
        ':authority': 'mydtu.duytan.edu.vn',
        ':method': 'POST',
        ':scheme': 'https',
        'accept': 'text/html, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'content-length': '7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://mydtu.duytan.edu.vn',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    page_studyingwarning = 'https://mydtu.duytan.edu.vn/sites/index.aspx?p=home_studyingwarning&functionid=113'
    page_warningDetail = 'https://mydtu.duytan.edu.vn/Modules/mentor/WarningDetail.aspx?'
    page_loadChuongTrinhHoc = 'https://mydtu.duytan.edu.vn/Modules/curriculuminportal/ajax/LoadChuongTrinhHoc.aspx?'

    def __init__(self, sessionId):
        """Khởi tạo một Session cho phép đăng nhập vào DTU thông qua sessionId.
        Sau khi đăng nhập xong, tự động chạy phương thức `getSpecialStudentID()` lấy
        specialNumber."""
        logging.info('init session and get special id')
        self.session = requests.Session()
        self.session.headers.update(CHROME_HEADER)
        requests.utils.add_dict_to_cookiejar(self.session.cookies, sessionId)
        self.specialNumber = self.getSpecialStudentID()

    def __getRequestToMyDTU(self, url, params=None):
        """Gởi một GET request tới MyDTU đi kèm params là các tham số được truyền vào dưới dạng một dict.
        Trả về HTML Page"""
        logging.info('send get request to {0}'.format(url))
        request = self.session.get(url, params=params)
        return request.text

    def __postRequestToMyDTU(self, url, params=None):
        """Gởi một POST request tới MyDTU đi kèm params là các tham số được truyền vào dưới dạng một dict.
        Trả về HTML Page"""
        logging.info('send post request to {0}'.format(url))
        request = self.session.post(url, params=params)
        return request.text  

    def getSpecialStudentID(self):
        """Trả về chuỗi đặc biệt được hash bởi một phương thức đặc biệt từ mã sinh viên."""
        logging.info('get special id')
        html = self.__getRequestToMyDTU(self.page_studyingwarning)
        soup = BeautifulSoup(html, 'lxml')
        warningTable = soup.find(class_='tbresult')
        tdHaveSpecialID = warningTable('td')[2]
        onClickValue = tdHaveSpecialID.span['onclick']
        return str(onClickValue).split("'")[1]

    def getStudentInfo(self) -> Dict:
        """Trả về một dict chứa thông tin cơ bản của sinh viên."""
        logging.info('get student infomation')
        specialStudentID = self.getSpecialStudentID()
        html = self.__getRequestToMyDTU(self.page_warningDetail, params={'stid':specialStudentID})
        soup = BeautifulSoup(html, 'lxml')
        warningTable = soup.find('table')
        tdList = warningTable('td')
        username = tdList[1].strong.text
        avatarBase64 = tdList[2].img['src']
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
        return output

    def getMajor(self) -> Dict:
        """Trả về một dict là ngành học của sinh viên."""
        logging.info('get major')
        html = self.__postRequestToMyDTU(self.page_loadChuongTrinhHoc, {'studentidnumber':self.specialNumber})
        soup = BeautifulSoup(html,'lxml')
        ul = soup.find('ul',class_='tabNavigation')
        return str(ul.li.a.text).strip()


    @staticmethod
    def toHTMLFile(filename: str, html: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(html))

    @staticmethod
    def saveBase64ToImage(base64Data: str, filename: str):
        imgdata = base64.decodebytes(base64Data)
        with open(filename, 'wb') as f:
            f.write(imgdata)


class DTUSummaryScore:
    """Class này đại diện cho điểm tổng kết của một học kỳ."""

    def __init__(self, listTrTagWithClassFooter: ResultSet):
        self.__listTrTagWithClassFooter = listTrTagWithClassFooter

    def getMeanSemesterScore(self):
        """Trung bình Điểm gốc Kỳ học."""
        return float(str(self.__listTrTagWithClassFooter[1]('td')[1].text).strip())

    def getMeanGPAScore(self):
        """Điểm Trung bình Tích lũy Kỳ học."""
        return float(str(self.__listTrTagWithClassFooter[2]('td')[1].text).strip())

    def getTotalCreditIsScored(self) -> int:
        """Tổng số Đơn vị Học tập (ĐVHT) có tính điểm (và có tính vào Tổng số ĐVHT):
        
        Điểm chữ: A+, A, A-, B+, B, B-, C+, C, C-, D, F	
        """
        return int(str(self.__listTrTagWithClassFooter[0]('td')[1].div.text).strip())

    def getTotalCreditIsNotScored(self):
        """Tổng số Đơn vị Học tập (ĐVHT) không tính điểm (và có tính vào Tổng số ĐVHT):
        
        Điểm chữ: P	
        """
        return int(str(self.__listTrTagWithClassFooter[3]('td')[1].div.text).strip())

    def getTotalCredit(self):
        """Tổng số Đơn vị Học tập (ĐVHT) Kỳ học."""
        return int(str(self.__listTrTagWithClassFooter[4]('td')[1].div.text).strip())

    def getTotalCreditPassAndIsNotScored(self):
        """Tổng số Đơn vị Học tập (ĐVHT) Đỗ không tính điểm (và không tính vào Tổng số ĐVHT):
        
        Điểm chữ: P (P/F)	
        """
        return int(str(self.__listTrTagWithClassFooter[5]('td')[1].div.text).strip())

    def getTotalCreditFailAndIsNotScored(self):
        """Tổng số Đơn vị Học tập (ĐVHT) bị Hỏng không tính điểm (và không tính vào Tổng số ĐVHT):
        
        Điểm chữ: F (P/F), W/R, I	
        """
        return int(str(self.__listTrTagWithClassFooter[6]('td')[1].div.text).strip())

    def getJson(self):
        return {
            "meanSemesterScore":self.getMeanSemesterScore(),
            "meanGPAScore":self.getMeanGPAScore(),
            "totalCreditIsScored":self.getTotalCreditIsScored(),
            "totalCreditIsNotScored":self.getTotalCreditIsNotScored(),
            "totalCredit":self.getTotalCredit(),
            "totalCreditPassAndIsNotScored":self.getTotalCreditPassAndIsNotScored(),
            "totalCreditFailAndIsNotScored":self.getTotalCreditFailAndIsNotScored()
        }


class DTUSubjectSCore:
    """Đại diện cho một hàng thể hiện thông tin điểm số của một môn trong bảng điểm."""

    def __init__(self, maMon:str = None, maLop:str=None, hinhThuc:str=None, tenMon:str=None, soDonViHocTap:int=None,
                loaiDonViHocTap:str=None, diemGoc:float=None, diemChu:str=None, diemQuyDoi:float=None, diemTichLuy:float=None):
        self.__maMon = maMon
        self.__maLop = maLop
        self.__hinhThuc = hinhThuc
        self.__tenMon = tenMon
        self.__soDonViHocTap = soDonViHocTap
        self.__loaiDonViHocTap = loaiDonViHocTap
        self.__diemGoc = diemGoc
        self.__diemChu = diemChu
        self.__diemQuyDoi = diemQuyDoi
        self.__diemTichLuy = diemTichLuy

    def __str__(self):
        return '<DTUSubjectSCore {0} {1}>'.format(self.maMon, self.tenMon)

    @property
    def maMon(self):
        return self.__maMon
    @property
    def maLop(self):
        return self.__maLop
    @property
    def hinhThuc(self):
        return self.__hinhThuc
    @property
    def tenMon(self):
        return self.__tenMon
    @property
    def soDonViHocTap(self):
        return self.__soDonViHocTap
    @property
    def loaiDonViHocTap(self):
        return self.__loaiDonViHocTap
    @property
    def diemGoc(self):
        return self.__diemGoc
    @property
    def diemChu(self):
        return self.__diemChu
    @property
    def diemQuyDoi(self):
        return self.__diemQuyDoi
    @property
    def diemTichLuy(self):
        return self.__diemTichLuy

    @maMon.setter
    def maMon(self, maMon:str):
        """Mã môn học CS 414."""
        self.__maMon = maMon
    @maLop.setter
    def maLop(self, maLop:str):
        self.__maLop = maLop
    @hinhThuc.setter
    def hinhThuc(self, hinhThuc:str):
        self.__hinhThuc = hinhThuc
    @tenMon.setter
    def tenMon(self, tenMon:str):
        self.__tenMon = tenMon
    @soDonViHocTap.setter
    def soDonViHocTap(self, soDonViHocTap: int):
        self.__soDonViHocTap = soDonViHocTap
    @loaiDonViHocTap.setter
    def loaiDonViHocTap(self, loaiDonViHocTap:str):
        self.__loaiDonViHocTap = loaiDonViHocTap
    @diemGoc.setter
    def diemGoc(self, diemGoc: float):
        self.__diemGoc = diemGoc
    @diemChu.setter
    def diemChu(self, diemChu:str):
        self.__diemChu = diemChu
    @diemQuyDoi.setter
    def diemQuyDoi(self, diemQuyDoi:float):
        self.__diemQuyDoi = diemQuyDoi
    @diemTichLuy.setter
    def diemTichLuy(self, diemTichLuy:float):
        self.__diemTichLuy = diemTichLuy

    def getJson(self):
        return {
            "maMon": self.__maMon,      
            "maLop": self.__maLop,
            "hinhThuc": self.__hinhThuc,
            "tenMon": self.__tenMon,
            "soDonViHocTap": self.__soDonViHocTap,
            "loaiDonViHocTap": self.__loaiDonViHocTap,
            "diemGoc": self.__diemGoc,
            "diemChu": self.__diemChu,
            "diemQuyDoi": self.__diemQuyDoi,
            "diemTichLuy": self.__diemTichLuy
        }
    
    def showSubjectScore(self):
        """In thông tin điểm số của môn này ra màn hình."""
        print("""Mã môn: {0}
                Mã lớp: {1}
                Hình thức: {2}
                Tên môn: {3}
                Số Đơn vị học tập (ĐVHT): {4}
                Loại Đơn vị học tập: {5}
                Điểm gốc: {6}
                Điểm chữ: {7}
                Điểm quy đổi: {8}
                Điểm tích luỹ: {9}""".format(self.__maMon,self.__maLop,self.__hinhThuc,self.__tenMon,self.__soDonViHocTap,
                                        self.__loaiDonViHocTap,self.__diemGoc,self.__diemChu,self.__diemQuyDoi,self.__diemTichLuy))
        

class DTUSemesterScore:
    """Bảng điểm trong một kỳ học."""

    def __init__(self, html) -> None:
        """Nhận vào HTML Page tương ứng với học kỳ đó."""
        self.__soup = BeautifulSoup(html, 'lxml')
        self.__listTrTagsWithClassDiem = self.__soup.find_all('tr', class_='diem')
        self.__listTrTagsWithClassFooter = self.__soup.find_all('tr', class_='footer')

    def getScoreJson(self):
        """Nhận về một json chứa toàn bộ thông tin điểm số của một học kỳ."""
        detailScore = [subjectScore.getJson() for subjectScore in self.getAllDTUSubjectScore()]
        summaryScore = self.getSummaryScore().getJson()
        return {
            "detailScore":detailScore,
            "summaryScore":summaryScore
        }

    def getSujectAt(self, index) -> DTUSubjectSCore:
        """Trả về một DTUSubjectScore tại hàng chỉ định. Nếu không trả về None."""
        try:
            trTag = self.__listTrTagsWithClassDiem[index]
            subjectScore = DTUSubjectSCore()
            subjectScore.maMon = str(trTag.td.div.text).strip()
            subjectScore.maLop = str(trTag('td')[1].div.div.text).strip()
            subjectScore.hinhThuc = str(trTag('td')[2].div.text).strip()
            subjectScore.tenMon = str(trTag('td')[3].div.text).strip()
            subjectScore.soDonViHocTap = int(str(trTag('td')[4].div.text).strip())
            subjectScore.loaiDonViHocTap = str(trTag('td')[5].div.text).strip()
            subjectScore.diemGoc = float(str(trTag('td')[6].div.text).strip())
            subjectScore.diemChu = str(trTag('td')[7].div.text).strip()
            subjectScore.diemQuyDoi = float(str(trTag('td')[8].div.text).strip())
            subjectScore.diemTichLuy = float(str(trTag('td')[9].div.text).strip())
            return subjectScore
        except:
            return None

    def getDTUSubjectScore(self, subjectId: str) -> DTUSubjectSCore:
        """Trả về một DTUSubjectScore object đại diện cho thông tin điểm số của một môn học trong học kỳ này. 
        Nếu subjectId không tồn tại trả về None."""
        for trTag in self.__listTrTagsWithClassDiem:
            if re.search('({})'.format(subjectId),str(self.__listTrTagsWithClassDiem[0].td.div.text).strip()):
                subjectScore = DTUSubjectSCore()
                subjectScore.maMon = str(trTag.td.div.text).strip()
                subjectScore.maLop = str(trTag('td')[1].div.div.text).strip()
                subjectScore.hinhThuc = str(trTag('td')[2].div.text).strip()
                subjectScore.tenMon = str(trTag('td')[3].div.text).strip()
                subjectScore.soDonViHocTap = int(str(trTag('td')[4].div.text).strip())
                subjectScore.loaiDonViHocTap = str(trTag('td')[5].div.text).strip()
                subjectScore.diemGoc = float(str(trTag('td')[6].div.text).strip())
                subjectScore.diemChu = str(trTag('td')[7].div.text).strip()
                subjectScore.diemQuyDoi = float(str(trTag('td')[8].div.text).strip())
                subjectScore.diemTichLuy = float(str(trTag('td')[9].div.text).strip())
                return subjectScore
            else:
                return None

    def getAllDTUSubjectScore(self) -> List[DTUSubjectSCore]:
        """Trả về một list chứa tất cả các DTUSubjectScore có trong học kỳ này."""
        output = []
        for trTag in self.__listTrTagsWithClassDiem:
            subjectScore = DTUSubjectSCore()
            subjectScore.maMon = str(trTag.td.div.text).strip()
            subjectScore.maLop = str(trTag('td')[1].div.div.text).strip()
            subjectScore.hinhThuc = str(trTag('td')[2].div.text).strip()
            subjectScore.tenMon = str(trTag('td')[3].div.text).strip()
            subjectScore.soDonViHocTap = int(str(trTag('td')[4].div.text).strip())
            subjectScore.loaiDonViHocTap = str(trTag('td')[5].div.text).strip()
            subjectScore.diemGoc = float(str(trTag('td')[6].div.text).strip())
            subjectScore.diemChu = str(trTag('td')[7].div.text).strip()
            subjectScore.diemQuyDoi = float(str(trTag('td')[8].div.text).strip())
            subjectScore.diemTichLuy = float(str(trTag('td')[9].div.text).strip())
            output.append(subjectScore)
        return output
    
    def getSummaryScore(self):
        """Trả về một DTUSummaryScore đại diện cho điểm tổng kết của học kỳ này."""
        return DTUSummaryScore(self.__listTrTagsWithClassFooter)

class DTUStudentScore(DTUSession):
    """Crawl thông tin bảng điểm của sinh viên."""

    def __init__(self, sessionId, specialNumber) -> None:
        super().__init__(sessionId)
        self.specialNumber = specialNumber
        self.__page = self.__getPage()
        self.__soup = BeautifulSoup(self.__page, 'lxml')
        self.__listSemesterParam = self.__getSemesterParams()

    def __getPage(self):
        """Phương thức này được chạy ngay sau khi khởi tạo đối tượng.
        Thực hiện lấy về HTML Page của trang điểm sinh viên.
        #### Không bao gồm các trang điểm chi tiết."""
        return self.get('https://mydtu.duytan.edu.vn/sites/index.aspx?p=home_bangdiem&functionid=14').text

    @staticmethod
    def __isLoadAjaxBangDiem(tag):
        """Lọc ra những thẻ <script> chứa hàm LoadAjaxBangDiem() để lấy ra tham số của chúng."""
        if re.search('(loadAjaxBangDiem\(\'[0-9]*\', \'[0-9]*\', \'[0-9]*\'\))', str(tag)) and tag.name == 'script':
            return True

    def __getSemesterParams(self) -> List[List[int]]:
        """Lấy ra list tham số tương ứng với từng học kỳ. 
        Tham số này sau đó được dùng cho các request để lấy về bảng điểm chi tiết cho từng học kỳ."""
        scriptLoadBangDiem = self.__soup.find_all(self.__isLoadAjaxBangDiem)
        listSemesterParams = []
        for tag in scriptLoadBangDiem:
            tag = ' '.join((str(tag).split()))
            functionLoadAjaxBangDiem = re.compile(r'>(.*?)<')
            group = functionLoadAjaxBangDiem.search(str(tag))
            listParams = str(group[1]).split("'")
            listSemesterParams.append([listParams[1],listParams[3], listParams[5]])
        return listSemesterParams

    def __getScoreTableHTMLPage(self, timespanid, curriculumid, specialNumber):
        url = 'https://mydtu.duytan.edu.vn/Modules/portal/ajax/LoadBangDiem.aspx?'
        params = {
            'timespanid':timespanid,
            'studentidnumber':specialNumber,
            'curriculumid':curriculumid
        }
        return self.post(url, params=params).text


    def getDTUSemesterScores(self) -> List[DTUSemesterScore]:
        """Trả về một list chứa các DTUSemesterScore."""
        output = []
        for listParam in self.__listSemesterParam:
            html = self.__getScoreTableHTMLPage(listParam[1], listParam[2], self.specialNumber)
            output.append(DTUSemesterScore(html))
        return output



if __name__ == "__main__":
    # demo get thong tin sinh vien
    # app = QApplication(sys.argv)
    # thread = thread_getSessionIdDTU.ThreadGetSessionIdDTU()

    # def getInfo(sessionID):
    #     dtu = DTUInfoStudent(sessionID)
    #     print(dtu.getMajor())
    #     app.exit()

    # def close(mess):
    #     print(mess)
    #     app.exit(1)

    # thread.signal_havedSessionId.connect(getInfo)
    # thread.signal_somethingError.connect(lambda: close('gap van de ve may chu hoac cookie'))
    # thread.signal_requestLogin.connect(lambda: close('yeu cau dang nhap'))
    # thread.signal_chromeIsNotFound.connect(lambda: close('yeu cau cai dat Chrome'))
    # thread.start()

    # app.exec()

    dtu = DTUStudentScore('điền sessionid','điền specialnumber')
    scores = dtu.getDTUSemesterScores()
    scores[0].getDTUSubjectScore('COM 101').showSubjectScore()