from PyQt5.QtCore import pyqtSignal, QObject


class InputRedirector(QObject):
    new_input = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.text = ""

    def readline(self):
        input_text = self.text
        self.text = ""
        return input_text

    # def flush(self):
    #     pass

    # def write(self, text):
    #     self.text += text
    #     if "\n" in self.text:
    #         self.new_input.emit(self.text)
    #         self.text = ""

    def set_text(self, text):
        self.text = text
        self.new_input.emit(text)
        # self.text = ""
