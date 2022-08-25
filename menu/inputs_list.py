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
from local_interface import LocalInterface
from PyQt6.QtGui import QIcon, QKeyEvent
from PyQt6 import QtGui
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QEvent
from interface import AefInterface
from page import Page

interface = LocalInterface()

class NoKeyPressCombo(QComboBox):

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        return QWidget.keyPressEvent(self, e)
    
    def __init__(self):
        super().__init__()


class Selector(QWidget):
    def changeLink(self, text):
        AefInterface.interface.update(self.input['name'], text)

    def __init__(self, input, commands):
        super().__init__()
        self.title = QLabel()
        if 'trigger' in input:
            self.title.setText(input['name'] + f" ({input['trigger']})")
        else:
            self.title.setText(input['name'] + f" ({input['left_trigger']},{input['right_trigger']})")

        self.input = input
        self.combo = NoKeyPressCombo()
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

class EncoderButtonList(Page):
    def __init__(self, changePage):
        super().__init__(changePage)
        buttons = AefInterface.interface.getInputsByType('button')
        encoders = AefInterface.interface.getInputsByType('encoder')

        bCommands = AefInterface.interface.getCommandsByInputType('button')
        eCommands = AefInterface.interface.getCommandsByInputType('encoder')

        self.lay = QGridLayout()

        self.bList = SelectorList(buttons, bCommands)
        self.eList = SelectorList(encoders, eCommands)

        self.lay.addWidget(self.bList, 0, 0)
        self.lay.addWidget(self.eList, 0, 1)

        self.setLayout(self.lay)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        return super().keyPressEvent(a0)