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
import aitpi
import json
import sys
from interface import AefInterface

class LocalInterface(AefInterface):
    """ Handles local aef manipulation
    """
    def init(self):
        """ What happens when a user starts the local app
        """
        effects = "../default_effects/"
        presets = "../default_presets/"
        recordings = "../recordings/"

        aef.run(effects, recordings, presets, sys.argv)
        aitpi.initInput('../example_input.json')

    def close(self):
        """ Close the interface
        """
        aef.shutdown()

    def update(self, key, value):
        """ Code called to update a buttons value

        Args:
            key (string): a valid input
            value (string): A valid command
        """
        aef.changeLink(key, value)

    def getCommnds(self):
        """ Gets commands from the backend
        """
        return aef.getCommands()

    def getInputs(self):
        """ Gets inputs from the backend
        """
        return aef.getInputs()
