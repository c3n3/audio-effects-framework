from json import encoder
import sys
from PyQt6.QtWidgets import *

from interface import AefInterface
from local_interface import LocalInterface
from inputs_list import EncoderButtonList
from start import Start


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bAndE = Start(self.changePage)
        self.setCentralWidget(self.bAndE)

    def changePage(self, page):
        self.setCentralWidget(page)

try:
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
finally:
    if AefInterface.interface != None:
        AefInterface.interface.close()
