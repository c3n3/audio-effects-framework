import os
from aef.constants import Constants
from aef.settings import GlobalSettings
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
        os.system("qjackctl --start --preset=guitar-module &")
        while (os.system("jack_control status >> {}".format(
            GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE
        )) != 0):
            pass
        command = ("pd {} -jack -nojackconnect -jackname global_pd {} >> {} &"
            .format("-nogui" if GlobalSettings.settings['debug_pd'] == 'False' else "",
                    GlobalSettings.settings['temp_dir'] + "/Global.pd",
                    GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))
        result = os.system(command)
        JackHandler.globalPdPid = os.popen("pidof pd").read()


    @staticmethod
    def jackConnectAll():
        """Makes the connections from system to user pd to global pd to output
           Do not run if user_pd is not started. Will potentially lead to deadlock
        """
        os.system("sh {}/jack_connect_all.sh >> {}".format(Constants.SCRIPTS_DIR,
            GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))

    @staticmethod
    def jackStop():
        """Stops jack
        """
        os.system("killall qjackctl >> {}".format(GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))
        os.system("jack_control stop >> {}".format(GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))

        
