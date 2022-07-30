from operator import truediv
import os
from time import sleep
from turtle import back
from aef.constants import Constants
from aef.settings import GS_temp, GlobalSettings
from aef.jack_node import JackNode
from aef import shell
from aef.log import *

class JackHandler():
    """Handles all things with jack
    """
    globalPdPid = -1

    @staticmethod
    def init():
        """Initializes the jack server
        """
        global settings
        shell.run(["killall", "pd"], expectFail=True)
        if (GlobalSettings.settings['use_qjack'] == 'True'):
            shell.run(["qjackctl", "--start", "--preset=guitar-module"], background=True)
        else:
            shell.run(["sh", "{}/jack_start.sh".format(GS_temp(Constants.SCRIPTS_DIR))])
        while (shell.run(["jack_control", "status"], expectFail=True).returncode != 0):
            sleep(0.1)
        command = " ".join([
            "pd",
            "-nogui" if GlobalSettings.settings['debug_pd'] == 'False' else "",
            "-jack",
            "-nojackconnect",
            "-jackname",
            "global_pd",
            GS_temp(Constants.GLOBAL_PD),
        ])
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
            if (i > 10):
                elog("Could not find user_pd or global_pd")
                break

        system = JackNode("system", 'playback', 'capture')

        JackNode.connect(userPd, globalPd)
        JackNode.connect(system, userPd)
        JackNode.connect(userPd, system)
        JackNode.connect(globalPd, system)


    @staticmethod
    def jackStop():
        """Stops jack
        """
        if (GlobalSettings.settings['use_qjack'] == 'True'):
            shell.run(["killall", "qjackctl"])
        shell.run(["jack_control", "stop"])
