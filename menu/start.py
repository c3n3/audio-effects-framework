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

from bluetooth_interface import BluetootInterface
from local_interface import LocalInterface
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui
from interface import AefInterface
from page import Page
from inputs_list import EncoderButtonList

localInterface = LocalInterface()
bluetoothInterface = BluetootInterface()

# class BlutoothSearchButton(QtWidgets.QPushButton):
#     def __init__(self):
#         super().__init__()

#     def mouseReleaseEvent(self, e) -> None:
#         print("Finding devices")
#         bluetoothInterface.searchForDevices()
#         print(bluetoothInterface.getFoundDevices())
#         return super().mouseReleaseEvent(e)


class Select(QtWidgets.QWidget):
    connect = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        bluetoothInterface.init()
        self.lay = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.Down)
        self.connectButton = QtWidgets.QPushButton()
        self.connectButton.setText("Connect to:")
        self.connectButton.clicked.connect(self.connectTo)
        self.combo = QtWidgets.QComboBox()
        self.lay.addWidget(self.connectButton)
        self.lay.addWidget(self.combo)
        self.setLayout(self.lay)
        self.conns = {}

    def connectTo(self):
        if len(self.conns) != 0:
            self.connect.emit(self.conns[self.combo.currentText()])

    def updateList(self, items):
        self.conns = items
        self.combo.clear()
        for connection in self.conns:
            self.combo.addItem(connection)

class Start(Page):
    def __init__(self, update):
        super().__init__(update)

        self.lay = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        self.localButton = QtWidgets.QPushButton()
        self.localButton.setText("Run locally")
        self.localButton.clicked.connect(self.runLocal)
        self.bluetoothSearch = QtWidgets.QPushButton()
        self.bluetoothSearch.setText("Search blutooth connections")
        self.bluetoothSearch.clicked.connect(self.getBtDevs)
        self.lay.addWidget(self.bluetoothSearch)
        self.connector = Select()
        self.connector.connect.connect(self.connect)
        self.lay.addWidget(self.connector)
        self.lay.addWidget(self.localButton)
        self.setLayout(self.lay)

    def runLocal(self):
        AefInterface.interface = localInterface
        localInterface.init()
        self.changePage(EncoderButtonList(self.changePage))

    def connect(self, addr):
        bluetoothInterface.connectTo(addr)
        AefInterface.interface = bluetoothInterface
        if bluetoothInterface.server.isConnected():
            self.changePage(EncoderButtonList(self.changePage))

    def getBtDevs(self):
        print("Searching")
        bluetoothInterface.searchForDevices()
        self.connector.updateList(bluetoothInterface.getFoundDevices())
        print("Got", bluetoothInterface.getFoundDevices())

