from json import encoder
import sys
from local_interface import LocalInterface
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QEvent

interface = LocalInterface()

class Selector(QWidget):

    def changeLink(self, text):
        interface.update(self.input['name'], text)

    def filter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            return False
        return True

    def __init__(self, input, commands):
        super().__init__()
        self.title = QLabel()
        if 'trigger' in input:
            self.title.setText(input['name'] + f" ({input['trigger']})")
        else:
            self.title.setText(input['name'] + f" ({input['left_trigger']},{input['right_trigger']})")

        self.input = input
        self.combo = QComboBox()
        self.combo.installEventFilter(self.filter)
        index = 0
        setVal = 0
        for command in commands:
            if command['name'] == self.input['reg_link']:
                setVal = index
            self.combo.addItem(command['name'])
            index += 1
        self.combo.setCurrentIndex(setVal)
        self.lay = QBoxLayout(QBoxLayout.Direction.Down)
        self.lay.addWidget(self.title)
        self.lay.addWidget(self.combo)
        self.setLayout(self.lay)
        self.combo.currentTextChanged.connect(self.changeLink)

class SelectorList(QWidget):
    def __init__(self, inputs, commands):
        super().__init__()
        self.selectors = QWidget()
        self.lay = QBoxLayout(QBoxLayout.Direction.Down)
        for input in inputs:
            sel = Selector(input, commands)
            self.lay.addWidget(sel)
            self.lay.setAlignment(sel, Qt.AlignmentFlag.AlignTop)
        self.selectors.setLayout(self.lay)
        self.setLayout(self.lay)

class EncoderButtonList(QWidget):
    def __init__(self):
        super().__init__()
        buttons = interface.getInputsByType('button')
        encoders = interface.getInputsByType('encoder')

        bCommands = interface.getCommandsByInputType('button')
        eCommands = interface.getCommandsByInputType('encoder')

        self.lay = QGridLayout()

        self.bList = SelectorList(buttons, bCommands)
        self.eList = SelectorList(encoders, eCommands)

        self.lay.addWidget(self.bList, 0, 0)
        self.lay.addWidget(self.eList, 0, 1)

        self.setLayout(self.lay)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bAndE = EncoderButtonList()
        self.setCentralWidget(self.bAndE)

try:
    interface.init()
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
finally:
    interface.close()
