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

from email.errors import NonPrintableDefect
import os
from re import S
from sys import stdout
from aef import shell


class JackNode:
    def __init__(self, name, inputName="input", outputName="output") -> None:
        self.name = name
        self.outputName = outputName
        self.inputName = inputName
        self.getInfo()

    def getInfo(self):
        self.outputs = self.getJackInfo(self.outputName)
        self.inputs = self.getJackInfo(self.inputName)

    def isValid(self, both=False):
        if not both:
            return len(self.outputs) + len(self.inputs) > 0
        return len(self.outputs) > 0 and len(self.inputs) > 0

    def getJackInfo(self, io):
        res = os.popen(f"jack_lsp | sed -nr 's/{self.name}:({io}.*?)/\\1/p'").read()
        res = res.split("\n")
        res.remove("")
        return res

    def get(self, io, index):
        if index < 0:
            return ""
        if io == "output":
            if index < len(self.outputs):
                return self.outputs[index]
            return self.get(io, index - 1)
        if io == "input":
            if index < len(self.inputs):
                return self.inputs[index]
            return self.get(io, index - 1)
        return ""

    @staticmethod
    def connect(source, sink):
        for i in range(max(len(source.outputs), len(sink.inputs))):
            run = [
                "jack_connect",
                f"{source.name}:{source.get('output', i)}",
                f"{sink.name}:{sink.get('input', i)}",
            ]
            shell.run(run)
