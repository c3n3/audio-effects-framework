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

from time import sleep
from aef.pd_handler import PdHandler
from aitpi import router
from aef.msg_list import EffectsMessage
from aef.pd_parser import PdParser
from aef.pd_routing_handler import PdRoutingHandler
from aef.log import *


class EffectsHandler:
    @staticmethod
    def consume(msg):
        if msg.event == "0":
            added = PdHandler.toggleFile(msg.name)
            PdHandler.parseFiles()
            if added and msg.name in PdParser.filesToHooks:
                dlog("Re-init hooks for", msg.name)
                sleep(0.2)
                for hook in PdParser.filesToHooks[msg.name]:
                    PdRoutingHandler.update(hook)

    @staticmethod
    def init():
        router.addConsumer([EffectsMessage.msgId], EffectsHandler)
