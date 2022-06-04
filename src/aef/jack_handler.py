import os
from time import sleep
from aef.constants import Constants
from aef.settings import GS_temp, GlobalSettings
from jack_node import JackNode
class JackHandler():
    """Handles all things with jack
    """
    globalPdPid = -1

    @staticmethod
    def init():
        """Initializes the jack server
        """
        global settings
        os.system("killall pd >> {}".format(GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))
        if (GlobalSettings.settings['use_qjack'] == 'True'):
            os.system("qjackctl --start --preset=guitar-module &")
        else:
            os.system("sh {}/jack_start.sh >> {}".format(GS_temp(Constants.SCRIPTS_DIR),
                GS_temp(Constants.SHELL_LOG_FILE)))
        while (os.system("jack_control status >> {}".format(
            GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE
        )) != 0):
            pass
        command = ("pd {} -jack -nojackconnect -jackname global_pd {} >> {} &"
            .format("-nogui" if GlobalSettings.settings['debug_pd'] == 'False' else "",
                    GS_temp(Constants.GLOBAL_PD),
                    GS_temp(Constants.SHELL_LOG_FILE)))
        result = os.system(command)
        JackHandler.globalPdPid = os.popen("pidof pd").read()


    @staticmethod
    def jackConnectAll():
        """Makes the connections from system to user pd to global pd to output
           Do not run if user_pd is not started. Will potentially lead to deadlock
        """
        userPd = JackNode("user_pd")
        i = 0
        while not userPd.isValid():
            userPd.getInfo()
            i += 0.5
            sleep(0.5)
            if (i > 10):
                print("Could not find user_pd")
                break

        globalPd = JackNode("global_pd")
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
            os.system("killall qjackctl >> {}".format(GS_temp(Constants.SHELL_LOG_FILE)))
        os.system("jack_control stop >> {}".format(GS_temp(Constants.SHELL_LOG_FILE)))


