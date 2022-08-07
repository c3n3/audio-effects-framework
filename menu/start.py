from bluetooth_interface import BluetootInterface
from local_interface import LocalInterface
from PyQt6 import QtWidgets
from page import Page

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


class Start(Page):

    def getBtDevs(self):
        print("Searching")
        bluetoothInterface.searchForDevices()
        print("Got", bluetoothInterface.getFoundDevices())

    def __init__(self, update):
        super().__init__(update)

        self.lay = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        self.bluetoothSearch = QtWidgets.QPushButton()
        self.bluetoothSearch.setText("Search blutooth connections")
        self.bluetoothSearch.clicked.connect(self.getBtDevs)
        self.lay.addWidget(self.bluetoothSearch)
        self.setLayout(self.lay)
