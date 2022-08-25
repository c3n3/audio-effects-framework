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

from aef.constants import Constants

name = Constants.DEFAULT_COMMAND_REGISTRY
file = """
[
    {
        "name": "loop",
        "type": "Sound recording",
        "input_type": "button",
        "id": "1001"
    },
    {
        "name": "record",
        "type": "Sound recording",
        "input_type": "button",
        "id": "1001"
    },
    {
        "name": "save",
        "type": "Sound recording",
        "input_type": "button",
        "id": "1003"
    },
    {
        "name": "volume",
        "type": "Sound recording",
        "input_type": "encoder",
        "id": "1001"
    }
]
"""
