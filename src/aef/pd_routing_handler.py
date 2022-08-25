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

import aitpi
from aef.constants import Constants
from aef.log import *
from aef.msg_list import PdRoutingMessage
from aitpi import router
from aef.pd_handler import PdHandler
from aef.pd_parser import PdParser
from aef.settings import GlobalSettings


class PdRoutingHandler:
    commandRegType = "Puredata Hooks"

    @staticmethod
    def update(hook):
        dlog("Updating hook", hook.routeId, hook.current)
        PdHandler.pdAction(hook.routeId, str(hook.current), 2999)

    @staticmethod
    def consume(msg):
        if msg.name in PdParser.hooks:
            hook = PdParser.hooks[msg.name]
            if msg.event == "LEFT":
                hook.down()
            elif msg.event == "RIGHT":
                hook.up()
            PdRoutingHandler.update(hook)

    @staticmethod
    def init():
        PdHandler.initHooks()
        router.addConsumer([PdRoutingMessage.msgId], PdRoutingHandler)

        aitpi.clearCommandTypeInRegistry(
            GlobalSettings.settings["temp_dir"] + Constants.TEMP_COMMAND_REG,
            PdRoutingHandler.commandRegType,
        )
        for key in PdParser.hooks.keys():
            hook = PdParser.hooks[key]
            aitpi.addCommandToRegistry(
                GlobalSettings.settings["temp_dir"] + Constants.TEMP_COMMAND_REG,
                hook.name,
                PdRoutingMessage.msgId,
                PdRoutingHandler.commandRegType,
                "encoder",
            )
