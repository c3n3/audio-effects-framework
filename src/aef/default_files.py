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

from aef import files
from aef.log import *
from aef.settings import GS_temp
import os

# Loop over all the modules inside the files folder, and output to temp
class DefaultFiles:
    @staticmethod
    def init():
        for file in files.files:
            try:
                os.makedirs(os.path.dirname(GS_temp(file.name)), exist_ok=True)
                f = open(GS_temp(file.name), "w")
                f.write(file.file)
                f.close()
            except:
                elog("Bad default file")
