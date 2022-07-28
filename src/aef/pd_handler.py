import os
from time import sleep
from aef.constants import Constants
from aef.settings import GlobalSettings
from aef.settings import GS_temp
from aef.pd_parser import PdParser
from aef.jack_handler import JackHandler
from aef.logger import Logger

class PdHandler():
    """Handles all pd functions
    """
    recording = False
    parser = PdParser()

    parser = PdParser()

    dir = None
    staticPd = GS_temp(Constants.DEFAULT_PD_DIR)

    files = []
    staticFiles = []

    def __init__ (self):
        """No init
        """
        raise Exception("No creating this object")

    @staticmethod
    def pdGlobalCommand(command):
        """A global PD comamnd
        """
        if (command == "RECORD"):
            PdHandler.record()
        elif (command == "PLAYBACK"):
            PdHandler.playback()

    @staticmethod
    def toggleFile(file):
        """Used to toggle an effect on or off
        """
        if (file in PdHandler.files):
            PdHandler.files.remove(file)
        else:
            PdHandler.files.append(file)
        print("Now contains: ", PdHandler.files)

    @staticmethod
    def initHooks():
        f = []
        try:
            for (dirpath, dirnames, filenames) in os.walk(PdHandler.dir):
                f.extend(filenames)
                break
        except:
            Logger.log("no pd files available", Logger.WARNING)
        parse = [f"{PdHandler.dir}/{x}" for x in f]
        parse.extend([f"{PdHandler.staticPd}/{x}" for x in PdHandler.staticFiles])
        PdHandler.parser.parseFiles(parse, None)

    @staticmethod
    def parseFiles():
        """Parses all PD files
        """
        parse = [f"{PdHandler.dir}/{x}" for x in PdHandler.files]
        parse.extend([f"{PdHandler.staticPd}/{x}" for x in PdHandler.staticFiles])
        PdHandler.parser.parseFiles(
            parse,
            GlobalSettings.settings['temp_dir'] + Constants.RESULT_PD)
        PdHandler.resetPuredata()

    @staticmethod
    def parseGlobals():
        """Used to append all global files
        """
        for root, dirs, files in os.walk(PdHandler.staticPd, topdown=False):
            for name in files:
                if ('.pd' in name):
                    PdHandler.staticFiles.append(name)

    @staticmethod
    def playback():
        """Used to playback the loop file
        """
        if (PdHandler.recording):
            PdHandler.record()
        PdHandler.pdAction("open loop.wav,start", 2999)

    @staticmethod
    def record():
        """Records audio
        """
        if (not PdHandler.recording):
            PdHandler.pdAction("open loop.wav,start")
        else:
            PdHandler.pdAction("stop")
        PdHandler.recording = not PdHandler.recording

    @staticmethod
    def killPuredata():
        """Kills the pd process
        """
        if (PdHandler.recording):
            PdHandler.record()
        pids = os.popen('pidof pd').read().split(" ")
        for pid in pids:
            if (pid != JackHandler.globalPdPid):
                os.system("sh {}/jack_disconnect_all.sh >> {}".format(
                    GS_temp(Constants.SCRIPTS_DIR),
                    GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))
                os.system('kill -9 {} >> {}'.format(
                    pid,
                    GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))
                os.system('wait {} >> {}'.format(
                    pid,
                    GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))
                sleep(0.2)

    @staticmethod
    def resetPuredata():
        PdHandler.pdAction("off", "", 2998)
        sleep(0.1)
        PdHandler.pdAction("on", "", 2998)

    @staticmethod
    def cleanUpPuredata():
        """Cleans up all instances of puredata.
        """
        os.system("killall pd >> {}".format(GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))

    @staticmethod
    def runPuredata():
        """Runs pd
        """
        global settings
        run = "pd {} -jack -nojackconnect -jackname user_pd {} >> {}&".format(
                "-nogui" if GlobalSettings.settings['debug_pd'] == 'False' else "",
                GlobalSettings.settings['temp_dir'] + Constants.TOP_PD,
                GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE
                )
        os.system(run)
        JackHandler.jackConnectAll()

    @staticmethod
    def pdAction(prefix, action, port = 3000): # this is for sending pd functions via a port
        """Sends pd action

        Args:
            prefix (str): The signifing prefx to tell pd what this is
            action (str): the action string
            port (int, optional): The port to send it over. Defaults to 3000.
        """
        command = "echo {} {} \; | pdsend {} >> {}".format(prefix, action, port,
            GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE)
        os.system(command)

    @staticmethod
    def initPd():
        JackHandler.init()
        PdHandler.dir = GlobalSettings.settings['effects_dir']
        PdHandler.parseGlobals()
        PdHandler.runPuredata()
        PdHandler.parseFiles()
        PdHandler.resetPuredata()
