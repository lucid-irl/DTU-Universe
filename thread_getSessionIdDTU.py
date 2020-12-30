from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from class_DTUWeb import DTULogin


class ThreadGetSessionIdDTU(QThread):
    """Khi triển khai Thread này bạn cần kết nối đầy đủ các signal được mô tả dưới đây với những behavior tương ứng.
    @signal_havedSessionId: Phát hiện được ASP.NET_SessionId của người dùng. Thứ được emit cùng với signal là
    sessionId đúng của người dùng là một dict như sau:

    `{'ASP.NET_SessionId':value}`
    
    @signal_somethingError: Có lỗi tất cả vấn đề thuộc về máy chủ, mạng mọc hoặc ASP.NET_SessionId.
    
    @signal_chromeIsNotFound: Chrome chưa được cài đặt trên máy tính.
    
    @signal_requestLogin: Yêu cầu người dùng đăng nhập."""

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
