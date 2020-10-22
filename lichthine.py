from bs4 import BeautifulSoup
import pandas as pd
import requests
from urllib.request import urlretrieve
from PyQt5 import QtCore, QtGui, QtWidgets

ROOT = 'http://pdaotao.duytan.edu.vn'


def get_url_sub(sub, id_, page):
    all_td_tag = []
    for i in range(1, page + 1):
        print('http://pdaotao.duytan.edu.vn/EXAM_LIST/?page={}&lang=VN'.format(i))
        r = requests.get('http://pdaotao.duytan.edu.vn/EXAM_LIST/?page={}&lang=VN'.format(i))
        soup = BeautifulSoup(r.text, 'html.parser')
        list_td_tag = soup.find_all('td', attrs={'style': 'padding-top:10px'})
        all_td_tag = all_td_tag + list_td_tag

    for td_tag in all_td_tag:
        if (((sub + str(id_)) in str(td_tag.a.contents[0])) or
                ((sub + str(id_)) in str(td_tag.a.contents[0])) or
                ((sub + str(id)) in str(td_tag.a.contents[0]))):
            print('\nComplete!!!')
            print(' '.join(str(td_tag.a.string).split()))
            print(str(td_tag.a['href']).replace('..', ROOT))
            return str(td_tag.a['href']).replace('..', ROOT)


def get_excel_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    list_span_tags = soup.find_all('span', class_='txt_l4')
    excel_url = list_span_tags[1].a['href'].replace('..', ROOT)
    return excel_url



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(748, 477)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(0, 10, 441, 391))
        self.comboBox.setObjectName("comboBox")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(180, 150, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 220, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 140, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 200, 81, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 50, 211, 20))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 310, 171, 61))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 748, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "mã lớp"))
        self.label_2.setText(_translate("MainWindow", "id lớp"))
        self.label_3.setText(_translate("MainWindow", "DTU assistant"))
        self.pushButton.setText(_translate("MainWindow", "tìm lịch"))
        self.pushButton.clicked.connect(self.timlich)
           
    def timlich(self):
        sub = self.lineEdit.text()
        id_ = self.lineEdit_2.text()
        sub = sub.upper()
        url = get_url_sub(sub, id_,4)
        if url == None:
            print('Khong tim thay mon nao nhu nay ({} {}) ca 😞'.format(sub, id_))

        else:
            print('get excel URL!!!')
            excel_url = get_excel_url(url)
            excel_url = excel_url.replace(' ', '%20')
            file_url = excel_url
            req = requests.get(file_url)
            with open('lichthine.xlsx', 'wb') as f:
                 f.write(req.content)
            file = open("lichthine.xlsx", "wb")    
            print('đã lưu file lịch thi vào máy của bạn!')



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
