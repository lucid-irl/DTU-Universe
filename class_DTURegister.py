from time import sleep
from typing import List
import dktc
from PyQt5.QtCore import QThread, pyqtSignal
import os
import pprint
import asyncio

class ThreadDTURegister(QThread):
    signal_Done = pyqtSignal('PyQt_PyObject')

    def __init__(self, culid, sessionid, listSubjectCode:List, captcha, studentid) -> None:
        QThread.__init__(self)
        self.culid = culid
        self.sessionId = sessionid
        self.listSubjectCode = listSubjectCode
        self.captcha = captcha
        self.studentid = studentid

    def run(self) -> None:
        dktc.addAccount(
        sessionId=self.sessionId,
        classRegCodes=self.listSubjectCode,
        studentIdNumber=self.studentid,
        curriculumId=self.culid,
        captcha=self.captcha
        )

    # You can add more addAccount() here

        loop = asyncio.get_event_loop()
        while True:
            result = loop.run_until_complete(dktc.registerAsync(loop, dktc.accounts))
            pprint(result)

            sleep(5) # Slow it down, don't be intensive!!!
            os.system('clear')
