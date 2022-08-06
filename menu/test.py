import sys
from local_interface import LocalInterface
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *

interface = LocalInterface()

class Button(QWidget):
    def __init__(self, input, commands):
        super().__init__()
        self.title = QLabel()
        self.title.setText(input['name'])
        self.combo = QComboBox()
        for command in commands:
            self.combo.addItem(command['name'])
        self.lay = QBoxLayout(QBoxLayout.Direction.Down)
        self.lay.addWidget(self.title)
        self.lay.addWidget(self.combo)
        self.setLayout(self.lay)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        commands = interface.getCommandsByInputType('button')
        inputs = interface.getInputsByType('button')
        print(inputs)
        self.buttons = QWidget()
        self.lay = QBoxLayout(QBoxLayout.Direction.Down)
        for input in inputs:
            self.lay.addWidget(Button(input, commands))
        self.buttons.setLayout(self.lay)
        self.setCentralWidget(self.buttons)

interface.init()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
interface.close()
