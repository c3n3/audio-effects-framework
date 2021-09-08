import os
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
        os.system("killall pd")
        os.system("qjackctl --start --preset=guitar-module &")
        while (os.system("jack_control status > /dev/null") != 0):
            pass
        command = ("pd {} -jack -nojackconnect -jackname global_pd {} &"
            .format("-nogui" if GlobalSettings.settings['debug_pd'].value == 'False' else "",
                    GlobalSettings.settings['global_pd'].value))
        result = os.system(command)
        JackHandler.globalPdPid = os.popen("pidof pd").read()


    @staticmethod
    def jackConnectAll():
        """Makes the connections from system to user pd to global pd to output
           Do not run if user_pd is not started. Will potentially lead to deadlock
        """
        os.system("sh {}/jack_connect_all.sh".format(GlobalSettings.settings['scripts_dir'].value))

    @staticmethod
    def jackStop():
        """Stops jack
        """
        os.system("killall qjackctl")
        os.system("jack_control stop")

        
