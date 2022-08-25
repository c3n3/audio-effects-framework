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

import os

class Constants:
    SRC_DIR = os.path.dirname(__file__)
    DEFAULT_PD_DIR = "default/"
    RESULT_PD = "master.pd"
    TOP_PD = "top.pd"
    SCRIPTS_DIR = "scripts/"
    RECORDING_DIR = "recordings/"
    GLOBAL_PD = "global.pd"
    DEFAULT_COMMAND_REGISTRY = "default_registry.json"
    TEMP_COMMAND_REG = "command_registry.temp.json"
    SHELL_LOG_FILE = "shell_out.log"
    PD_LOG_FILE = "pd_out.log"
