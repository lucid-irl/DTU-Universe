from bs4.element import ResultSet
from class_DTUWeb import DTUSession
from typing import Dict, List
from bs4 import BeautifulSoup

import logging
import base64
import re
import json

logging.basicConfig(level=logging.INFO)

class DTUInfoStudent(DTUSession):
    """Class này chịu trách nhiệm lấy thông tin của sinh viên DTU."""

    PAGE_STUDYING_WARNING = 'https://mydtu.duytan.edu.vn/sites/index.aspx?p=home_studyingwarning&functionid=113'
    PAGE_WARNING_DETAIL = 'https://mydtu.duytan.edu.vn/Modules/mentor/WarningDetail.aspx?'
    PAGE_STUDYING_PROGRAM = 'https://mydtu.duytan.edu.vn/Modules/curriculuminportal/ajax/LoadChuongTrinhHoc.aspx?'

    def __init__(self, ASPNETSessionIdDict):
        """Khởi tạo một Session cho phép đăng nhập vào DTU thông qua ASPNETSessionIdDict.
        Sau khi đăng nhập xong, tự động chạy phương thức `getSpecialStudentID()` lấy
        specialNumber."""
        super().__init__(ASPNETSessionIdDict)
        self.__soup = BeautifulSoup(self.__getPage(), 'lxml')
        self.specialStudentID = self.getSpecialStudentID()
        html = self.get(self.PAGE_WARNING_DETAIL, params={'stid':self.specialStudentID}).text
        self.__soupPageWarningDetail = BeautifulSoup(html, 'lxml')

    def __getPage(self):
        return self.get(self.PAGE_STUDYING_WARNING).text

    def getJson(self) -> Dict:
        """Trả về JSON chứa thông tin sinh viên."""
        logging.info('get student infomation')

        warningTable = self.__soupPageWarningDetail.find('table')
        tdList = warningTable('td')
        username = tdList[1].strong.text
        # avatarBase64 = tdList[2].img['src']
        studentID = tdList[4].text
        birthday = str(tdList[6].text).strip()
        cmnd = tdList[8].text
        dtuMail = tdList[10].a.text
        numberPhone = tdList[12].text
        location = str(tdList[15].text).strip()
        return {
                'student_id':studentID,
                'username':username,
                'special_number':self.specialStudentID,
                'birthday':birthday,
                'cmnd':cmnd,
                'email':dtuMail,
                'number_phone':numberPhone,
                'location':location,
                'mentor':self.getMentor(),
                'degree':self.getDegree()
            }

    def getMentor(self):
        """Trả về tên giảng viên cố vấn của sinh viên này."""
        return str(self.__soup.find('div', class_='mentorname').text).split(':')[1].strip()

    def getSpecialStudentID(self):
        """Trả về chuỗi đặc biệt được hash bởi một phương thức đặc biệt từ mã sinh viên."""
        logging.info('get special id')
        warningTable = self.__soup.find(class_='tbresult')
        tdHaveSpecialID = warningTable('td')[2]
        onClickValue = tdHaveSpecialID.span['onclick']
        return str(onClickValue).split("'")[1]
    
    def getStudentId(self):
        return self.getJson()['student_id']

    def getUsername(self):
        return self.getJson()['username']

    def getSpecialNumber(self):
        return self.getJson()['special_number']

    def getBirthday(self):
        return self.getJson()['birthday']

    def getCMND(self):
        return self.getJson()['cmnd']

    def getEmail(self):
        return self.getJson()['email']

    def getNumberphone(self):
        return self.getJson()['number_phone']

    def getLocation(self):
        return self.getJson()['location']

    def getDegree(self):
        tableTag = self.__soup.find('table', class_='tbresult')
        return str(tableTag('td')[3].a.text).strip()

    def toJsonFile(self):
        with open(self.getStudentId()+'.json', 'w', encoding='utf-8') as f:
            json.dump(self.getJson(),f, indent=4, ensure_ascii=False)

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


class DTUSubjectScore:
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
        return '<DTUSubjectScore {0} {1}>'.format(self.maMon, self.tenMon)

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
        """Mã môn học.
        
        Ví dụ CS 414
        """
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
                self.__maMon:{
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
                }
    
    def showSubjectScore(self):
        """In thông tin điểm số của môn này ra màn hình."""
        info = """Mã môn: {0}\nMã lớp: {1}\nHình thức: {2}\nTên môn: {3}\nSố Đơn vị học tập (ĐVHT): {4}\n
        Loại Đơn vị học tập: {5}\nĐiểm gốc: {6}\nĐiểm chữ: {7}\nĐiểm quy đổi: {8}\nĐiểm tích luỹ: {9}"""
        info.format(self.__maMon,self.__maLop,self.__hinhThuc,self.__tenMon,self.__soDonViHocTap,
                    self.__loaiDonViHocTap,self.__diemGoc,self.__diemChu,self.__diemQuyDoi,self.__diemTichLuy)
        print(info)
        

class DTUSemesterScore:
    """Bảng điểm trong một kỳ học."""

    def __init__(self, html, id, description) -> None:
        """Nhận vào HTML Page tương ứng với học kỳ đó."""
        self.__id = id
        self.__description = description
        self.__soup = BeautifulSoup(html, 'lxml')
        self.__listTrTagsWithClassDiem = self.__soup.find_all('tr', class_='diem')
        self.__listTrTagsWithClassFooter = self.__soup.find_all('tr', class_='footer')

    def getJson(self):
        """Nhận về một json chứa toàn bộ thông tin điểm số của một học kỳ."""
        detailScore = {}
        for subjectScore in self.getAllDTUSubjectScore():
            detailScore.update(subjectScore.getJson())
        summaryScore = self.getSummaryScore().getJson()
        return {
                self.__id: {
                    "detail":detailScore,
                    "summary":summaryScore,
                    "description":self.__description
                    }
                }

    def getSujectAt(self, index) -> DTUSubjectScore:
        """Trả về một DTUSubjectScore tại hàng chỉ định. Nếu không trả về None."""
        try:
            trTag = self.__listTrTagsWithClassDiem[index]
            subjectScore = DTUSubjectScore()
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

    def getDTUSubjectScore(self, subjectId: str) -> DTUSubjectScore:
        """Trả về một DTUSubjectScore object đại diện cho thông tin điểm số của một môn học trong học kỳ này. 
        Nếu subjectId không tồn tại trả về None."""
        for trTag in self.__listTrTagsWithClassDiem:
            if re.search('({})'.format(subjectId),str(self.__listTrTagsWithClassDiem[0].td.div.text).strip()):
                subjectScore = DTUSubjectScore()
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

    def getAllDTUSubjectScore(self) -> List[DTUSubjectScore]:
        """Trả về một list chứa tất cả các DTUSubjectScore có trong học kỳ này."""
        output = []
        for trTag in self.__listTrTagsWithClassDiem:
            subjectScore = DTUSubjectScore()
            subjectScore.maMon = str(trTag.td.div.text).strip()
            subjectScore.maLop = str(trTag('td')[1].div.div.text).strip()
            if str(trTag('td')[2].div.text).strip():
                subjectScore.hinhThuc = str(trTag('td')[2].div.text).strip()
            else:
                subjectScore.hinhThuc = 'NaN'
            subjectScore.tenMon = str(trTag('td')[3].div.text).strip()
            subjectScore.soDonViHocTap = int(str(trTag('td')[4].div.text).strip())
            subjectScore.loaiDonViHocTap = str(trTag('td')[5].div.text).strip()
            if str(trTag('td')[6].div.text).strip():
                subjectScore.diemGoc = float(str(trTag('td')[6].div.text).strip())
            else:
                subjectScore.diemGoc = 'NaN'
            subjectScore.diemChu = str(trTag('td')[7].div.text).strip()
            if str(trTag('td')[8].div.text).strip():
                subjectScore.diemQuyDoi = float(str(trTag('td')[8].div.text).strip())
            else:
                subjectScore.diemQuyDoi = 'NaN'
            if str(trTag('td')[9].div.text).strip():
                subjectScore.diemTichLuy = float(str(trTag('td')[9].div.text).strip())
            else:
                subjectScore.diemTichLuy = 'NaN'
            output.append(subjectScore)
        return output
    
    def getSummaryScore(self):
        """Trả về một DTUSummaryScore đại diện cho điểm tổng kết của học kỳ này."""
        return DTUSummaryScore(self.__listTrTagsWithClassFooter)


class DTUStudentScore(DTUSession):
    """Crawl thông tin bảng điểm của sinh viên."""

    def __init__(self, ASPNETSessionIdDict, specialNumber) -> None:
        super().__init__(ASPNETSessionIdDict)
        self.specialNumber = specialNumber
        self.__soup = BeautifulSoup(self.__getPage(), 'lxml')
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
        infoes = self.getSemesterInfo()
        self.output = []
        for i in range(len(self.__listSemesterParam)):
            description = infoes[i]
            html = self.__getScoreTableHTMLPage(self.__listSemesterParam[i][1], self.__listSemesterParam[i][2], self.specialNumber)
            self.output.append(DTUSemesterScore(html, i, description))
        return self.output

    def getSummary(self) -> Dict[str,str]:
        """Trả về dict chứa thông tin bảng điểm."""
        listTrTagWithClassFooter = self.__soup.find_all('tr', class_='footer')
        totalCreditIsScored = {
            'description':str(listTrTagWithClassFooter[0].td.text).strip(),
            'number': int(str(listTrTagWithClassFooter[0]('td')[1].div.text)),
            'unit': str(listTrTagWithClassFooter[0]('td')[2].div.text).strip()
            }
        totalCreditFailButAgainAndPass = {
            'description':str(listTrTagWithClassFooter[1].td.text).strip(),
            'number': int(str(listTrTagWithClassFooter[1]('td')[1].div.text)),
            'unit': str(listTrTagWithClassFooter[1]('td')[2].div.text).strip()
        }
        totalCreditIsNotScored = {
            'description':str(listTrTagWithClassFooter[2].td.text).strip(),
            'number': int(str(listTrTagWithClassFooter[2]('td')[1].div.text)),
            'unit': str(listTrTagWithClassFooter[2]('td')[2].div.text).strip()
        }
        totalCreditForAllSemester = {
            'description':str(listTrTagWithClassFooter[3].td.b.text).strip(),
            'number': int(str(listTrTagWithClassFooter[3]('td')[1].div.b.text)),
            'unit': str(listTrTagWithClassFooter[3]('td')[2].div.b.text).strip()
        }
        rootMeanForAllSemester = {
            'description':str(listTrTagWithClassFooter[4].td.b.text).strip(),
            'number': float(str(listTrTagWithClassFooter[4]('td')[1].div.b.text)),
            'unit':'NaN'
        }
        accumulateMeanForAllSemester = {
            'description':str(listTrTagWithClassFooter[5].td.b.text).strip(),
            'number': float(str(listTrTagWithClassFooter[5]('td')[1].div.b.text)),
            'unit':'NaN'
        }
        totalCreditPassNotScored = {
            'description':str(listTrTagWithClassFooter[6].td.text).strip(),
            'number': int(str(listTrTagWithClassFooter[6]('td')[1].div.text)),
            'unit': str(listTrTagWithClassFooter[6]('td')[2].div.text).strip()
        }
        totalCreditFailNotScored = {
            'description':str(listTrTagWithClassFooter[7].td.text).strip(),
            'number': int(str(listTrTagWithClassFooter[7]('td')[1].div.text)),
            'unit': str(listTrTagWithClassFooter[7]('td')[2].div.text).strip()
        }
        return {
            'totalCreditIsScored':totalCreditIsScored,
            'totalCreditFailButAgainAndPass':totalCreditFailButAgainAndPass,
            'totalCreditIsNotScored':totalCreditIsNotScored,
            'totalCreditForAllSemester':totalCreditForAllSemester,
            'rootMeanForAllSemester':rootMeanForAllSemester,
            'accumulateMeanForAllSemester':accumulateMeanForAllSemester,
            'totalCreditPassNotScored':totalCreditPassNotScored,
            'totalCreditFailNotScored':totalCreditFailNotScored
        }
        
    def getSemesterInfo(self) -> List[str]:
        """Trả về một list chưa thông tin tên học kỳ."""
        def __mapGetSemesterName(trtag):
            return str(trtag.td.text).strip()
        listTrTag = self.__soup.find_all('tr', class_='hocky')
        return list(map(__mapGetSemesterName, listTrTag))

    def getJson(self):
        """Trả về cấu trúc JSON của toàn bộ bảng điểm."""
        semesters = {}
        for semesterScore in self.getDTUSemesterScores():
            semesters.update(semesterScore.getJson())
        self.getSummary()
        return {
                "score_table": {
                    "semesters":semesters,
                    "summary":self.getSummary()
                    }
                }


class DTUGetAll:

    def __init__(self, ASPNETSessionIdDict) -> None:
        self.ASPNETSessionIdDict = ASPNETSessionIdDict

    def getJson(self):
        dtust = DTUInfoStudent(self.ASPNETSessionIdDict)
        dtusc = DTUStudentScore(ASPNETSessionIdDict=self.ASPNETSessionIdDict,specialNumber=dtust.getSpecialNumber())
        jsonOut = dtust.getJson()
        jsonOut.update(dtusc.getJson())
        return jsonOut

    def toFile(self, JSONFilename: str = 'DTUGetAll_info.json'):
        try:
            logging.info('toFile() --> {0}'.format(JSONFilename))
            with open(JSONFilename, 'w', encoding='utf-8') as f:
                json.dump(self.getJson(), f, ensure_ascii=False, indent=4)
        except:
            print('Can not write info on {0}'.format(JSONFilename))

if __name__ == "__main__":
    js = DTUInfoStudent({'ASP.NET_SessionId':'d5fesmaw42zcbwv5cquifuxs'}).getStudentId()

