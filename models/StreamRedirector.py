from PyQt5.QtCore import pyqtSignal, QObject


class StreamRedirector(QObject):
    stdout = pyqtSignal(str)
    stderr = pyqtSignal(str)
    stdin = pyqtSignal()
    def write(self, text):
        self.stdout.emit(text)

    def flush(self):
        pass

    def __del__(self):
        pass