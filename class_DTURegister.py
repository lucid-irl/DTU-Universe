import asyncio
from PyQt5.QtCore import QThread, pyqtSignal

async def sendRequest():
    print('Send request register!!!')
    await asyncio.sleep(4)
    print('Success')

async def register(subject: str):
    print(subject)
    await sendRequest()
    return 1

async def main():
    subjects = ['CS 132', 'HG123', 'OJU 412']
    await asyncio.gather(*(register(subject) for subject in subjects))

class ThreadDTURegister(QThread):
    signal_Done = pyqtSignal('PyQt_PyObject')

    def __init__(self) -> None:
        QThread.__init__(self)

    def run(self) -> None:
        r = asyncio.run(main())
        self.signal_Done.emit(r)
