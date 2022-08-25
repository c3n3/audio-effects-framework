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


# A very simple example of how to setup the aef

#!/usr/bin/python3
import aef
import aitpi
import sys

effects = "../default_effects/"
presets = "../default_presets/"
recordings = "./recordings/"

def init():
    print("args", sys.argv)
    aef.run(effects, recordings, presets, sys.argv)

init()
aitpi.initInput('input.json')

try:
    while (True):
            name = input("Name: ")
            value = input("Value: ")
            aef.changeLink(name, value)
except:
    print("Shutting down")

aef.shutdown()
