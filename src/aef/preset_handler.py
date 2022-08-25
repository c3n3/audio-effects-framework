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

from aef.msg_list import PresetMessage
from aitpi import router
from aef.pd_handler import PdHandler


class PresetHandler:
    @staticmethod
    def consume(msg):
        """Handles actually running the preset commands that are sent through the CentralRouter

        Args:
            msg (Message): Message containing the preset to run
        """
        if msg.event == "1":
            return
        f = open(msg.attributes["path"] + msg.name, "r")
        lines = f.readlines()
        PdHandler.files = []
        for i in range(0, len(lines)):
            PdHandler.toggleFile(lines[i].replace("\n", ""))
        PdHandler.parseFiles()

    @staticmethod
    def init():
        router.addConsumer([PresetMessage.msgId], PresetHandler)
