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
import sys

class AefInterface():
    interface = None

    """ Handles local aef manipulation
    """
    def init(self):
        """ What happens when a user starts the local app
        """
        pass

    def close(self):
        """ Close the interface
        """
        pass

    def update(self, key, value):
        """ Code called to update an inputs value

        Args:
            key (string): a valid input
            value (string): A valid command
        """
        pass

    def getCommnds(self):
        """ Gets commands from the backend
        """
        pass

    def getInputsByType(self, type):
        inputs = self.getInputs()

        ret = []
        for input in inputs:
            if input['type'] == type:
                ret.append(input)
        return ret

    def getCommandsByInputType(self, inType):
        commands = self.getCommnds()

        ret = []
        for command in commands:
            if command['input_type'] == inType:
                ret.append(command)
        return ret

    def getInputs(self):
        """ Gets inputs from the backend
        """
        pass
