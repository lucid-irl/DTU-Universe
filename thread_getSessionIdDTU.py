
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from class_DTUWeb import DTULogin


class ThreadGetSessionIdDTU(QThread):

    signal_havedSessionId = pyqtSignal('PyQt_PyObject')
    signal_somethingError = pyqtSignal('PyQt_PyObject')
    signal_chromeIsNotFound = pyqtSignal('PyQt_PyObject')
    signal_requestLogin = pyqtSignal('PyQt_PyObject')
    dtuLogin = DTULogin()

    def __init__(self) -> None:
        QThread.__init__(self)

    def run(self) -> None:
        currentCookies = self.dtuLogin.getCookiesFromChrome()
        sessionIdDTU = self.dtuLogin.getDTUSessionIDFromCookies(currentCookies)
        if currentCookies:
            if sessionIdDTU:
                if self.dtuLogin.isCanLoginDTU(sessionIdDTU):
                    self.signal_havedSessionId.emit(sessionIdDTU)
                else:
                    self.signal_somethingError.emit(True)
            else:
                self.signal_requestLogin.emit(True)
        else:
            self.signal_chromeIsNotFound.emit(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    def close(mess):
        print(mess)
        app.exit(1)
    thread = ThreadGetSessionIdDTU()
    thread.signal_havedSessionId.connect(lambda s: close('day la session id: {0}'.format(s)))
    thread.signal_somethingError.connect(lambda: close('gap van de ve may chu hoac cookie'))
    thread.signal_requestLogin.connect(lambda: close('yeu cau dang nhap'))
    thread.signal_chromeIsNotFound.connect(lambda: close('yeu cau cai dat Chrome'))
    thread.start()
    app.exec()