import os
from time import sleep
from aef.constants import Constants
from aef.settings import GS_temp, GlobalSettings
from aef.jack_node import JackNode
from aef.common import runSilent
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
        runSilent("killall pd")
        if (GlobalSettings.settings['use_qjack'] == 'True'):
            runSilent("qjackctl --start --preset=guitar-module &")
        else:
            runSilent("sh {}/jack_start.sh >> {}".format(GS_temp(Constants.SCRIPTS_DIR),
                GS_temp(Constants.SHELL_LOG_FILE)))
        while (runSilent("jack_control status").returncode != 0):
            sleep(0.1)
        command = ("pd {} -jack -nojackconnect -jackname global_pd {} >> {} &"
            .format("-nogui" if GlobalSettings.settings['debug_pd'] == 'False' else "",
                    GS_temp(Constants.GLOBAL_PD),
                    GS_temp(Constants.SHELL_LOG_FILE)))
        runSilent(command)
        JackHandler.globalPdPid = os.popen("pidof pd").read()


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
            runSilent("killall qjackctl")
        runSilent("jack_control stop")
