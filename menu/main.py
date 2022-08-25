# Audio Effects Framework - A python library to setup Puredata effects
# Copyright (C) 2022  Caden Churchman
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
