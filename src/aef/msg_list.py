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

from aitpi import Message


class InputPuredataMessage(Message):
    """Handles input puredata
    """

    msgId = 1001


class PresetMessage(Message):
    """Handles running presets
    """

    msgId = 1002


class RecordingMessage(Message):
    """When the user issues some recording command
    """

    msgId = 1003


class OutputMessage(Message):
    """No data messsages
    """

    msgId = 1004

class EffectsMessage(Message):
    """ Handles effects
    """

    msgId = 1005


class PdRoutingMessage(Message):
    """ Handles effects
    """

    msgId = 1006
