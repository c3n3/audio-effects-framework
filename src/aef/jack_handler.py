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
from time import sleep
from aef.constants import Constants
from aef.settings import GS_temp, GlobalSettings
from aef.jack_node import JackNode
from aef import shell
from aef.log import *


class JackHandler:
    """Handles all things with jack
    """

    globalPdPid = -1
    jackdProc = None

    @staticmethod
    def init():
        """Initializes the jack server
        """
        global settings
        shell.run(["killall", "pd"], expectFail=True)
        jackCommand = ""
        file = GlobalSettings.settings["jackdrc"]
        try:
            with open(file, "r") as f:
                jackCommand = f.read()
            jackCommand = jackCommand.split()
        except FileNotFoundError:
            elog("No .jackdr in", file, "- cannot start")
            exit(1)
        JackHandler.jackdProc = shell.run(jackCommand, background=True)

        timeout = 10
        while shell.run(["jack_lsp"], expectFail=True).returncode != 0:
            sleep(0.1)
            timeout -= 0.1
            if timeout < 0:
                elog("Jack did not properly start")

        command = " ".join(
            [
                "pd",
                "-nogui" if GlobalSettings.settings["debug_pd"] == "False" else "",
                "-jack",
                "-nojackconnect",
                "-jackname",
                "global_pd",
                GS_temp(Constants.GLOBAL_PD),
            ]
        )
        JackHandler.globalPdPid = shell.run(command, background=True, shell=True).pid

    @staticmethod
    def jackConnectAll():
        """Makes the connections from system to user pd to global pd to output
           Do not run if user_pd is not started. Will potentially lead to deadlock
        """
        userPd = JackNode("user_pd")
        globalPd = JackNode("global_pd")
        i = 0
        while not userPd.isValid(True) or not globalPd.isValid(True):
            userPd.getInfo()
            globalPd.getInfo()
            i += 0.5
            sleep(0.5)
            if i > 10:
                elog("Could not find user_pd or global_pd")
                break

        system = JackNode("system", "playback", "capture")

        JackNode.connect(userPd, globalPd)
        JackNode.connect(system, userPd)
        JackNode.connect(userPd, system)
        JackNode.connect(globalPd, system)

    @staticmethod
    def jackStop():
        """Stops jack
        """
        if JackHandler.jackdProc != None:
            JackHandler.jackdProc.kill()
            JackHandler.jackdProc.wait()
