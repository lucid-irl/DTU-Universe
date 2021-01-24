from class_dialogNotification import NotificationWindow
from PyQt5.QtCore import QThread, pyqtSignal

class ThreadDTURegister(QThread):
    signal_Done = pyqtSignal('PyQt_PyObject')

    def __init__(self) -> None:
        QThread.__init__(self)

    def run(self) -> None:
        NotificationWindow('Thật là buồn','Đây là một tính năng thử nghiệm và sẽ đéo bao giờ có trên đời này, huhu').exec()
