from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
class main_view(QMainWindow):
    def __init__(self):
        super(main_view, self).__init__()
        uic.loadUi("views/main.ui", self)