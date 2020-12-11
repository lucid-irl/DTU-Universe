
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from class_dtuWeb import DTULogin


class ThreadGetSessionIdDTU(QThread):

    signal_havedSessionId = pyqtSignal('PyQt_PyObject')
    signal_requestLoginDTU = pyqtSignal('PyQt_PyObject')
    signal_chromeIsNotFound = pyqtSignal('PyQt_PyObject')
    signal_serverIsHavingProblem = pyqtSignal('PyQt_PyObject')
    dtuLogin = DTULogin()

    def __init__(self) -> None:
        QThread.__init__(self)

    def run(self) -> None:
        currentCookies = self.dtuLogin.getCookiesFromChrome()

        if currentCookies:
            if self.dtuLogin.isCanLoginDTU(currentCookies):
                print('dang nhap thanh cong')
            else:
                self.signal_serverIsHavingProblem.emit(True)
            if self.dtuLogin.isDTUCookiesTrue(currentCookies):
                sessionIdDTU = self.dtuLogin.getDTUSessionIDFromCookies(currentCookies)
                self.signal_havedSessionId.emit(sessionIdDTU)
            else:
                print(self.dtuLogin.getDTUSessionIDFromCookies(currentCookies))
                self.signal_requestLoginDTU.emit(True)
        else:
            self.signal_chromeIsNotFound.emit(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    def close(mess):
        print(mess)
        app.exit(1)
    thread = ThreadGetSessionIdDTU()
    thread.signal_requestLoginDTU.connect(lambda: close('yeu cau dang nhap dtu'))
    thread.signal_havedSessionId.connect(lambda s: close('day la session id: {0}'.format(s)))
    thread.signal_serverIsHavingProblem.connect(lambda: close('gap van de ve may chu'))
    thread.start()
    app.exec()