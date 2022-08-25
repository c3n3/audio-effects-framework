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

import aef
import sys
import os
import aitpi
from aitpi import router
from aef.pd_parser import PdParser
from aef.log import *
from aef import shell
from aef import blutooth_control
import time

from aef import commands
from aef.msg_list import Message

class OutputWatch:
    def consume(self, msg):
        pass
try:
    dirname = os.path.dirname(__file__)
    recordingsFolder = os.path.join(dirname, "../../recordings/")
    effectsFolder = os.path.join(dirname, "../../default_effects/")
    presetsFolder = os.path.join(dirname, "../../default_presets/")
    aef.run(effectsFolder, recordingsFolder, presetsFolder, sys.argv)
    inputJson = os.path.join(dirname, "../../example_input.json")
    aitpi.initInput(inputJson)
    router.addConsumer([1004], OutputWatch())

    if GlobalSettings.settings["bluetooth"] == "True":
        blutooth_control.run()
    else:
        while True:
            aitpi.takeInput(input("Input: "))
except KeyboardInterrupt:
    pass
finally:
    pass
    aef.shutdown()
