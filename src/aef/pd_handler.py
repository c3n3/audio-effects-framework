import os
from time import sleep
from aef.settings import GlobalSettings
from aef.puredata_parser import PuredataParser
from aef.jack_handler import JackHandler

class PdHandler():
    """Handles all pd functions
    """
    recording = False

    parser = PuredataParser()

    dir = None
    staticPd = './aef/Default/'

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

    @staticmethod
    def parseFiles():
        """Parses all PD files
        """
        PuredataParser.parse(
            PdHandler.files,
            PdHandler.dir,
            PdHandler.staticFiles,
            PdHandler.staticPd,
            GlobalSettings.settings['result_pd'].value)
        PdHandler.killPuredata()
        print("Running pd")
        PdHandler.runPuredata()

    @staticmethod
    def parseGlobals():
        """Used to append all global files
        """
        for root, dirs, files in os.walk(PdHandler.staticPd, topdown=False):
            for name in files:
                print("name:", name)
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
                os.system("sh {}/jack_disconnect_all.sh".format(GlobalSettings.settings['scripts_dir'].value))
                os.system('kill {}'.format(pid))
                os.system('wait {}'.format(pid))
                sleep(0.2)

    @staticmethod
    def cleanUpPuredata():
        """Cleans up all instances of puredata.
        """
        os.system("killall pd")

    @staticmethod
    def runPuredata():
        """Runs pd
        """
        global settings
        os.system("pd {} -jack -nojackconnect -jackname user_pd {} &"
            .format(
                "-nogui" if GlobalSettings.settings['debug_pd'].value == 'False' else "",
                GlobalSettings.settings['result_pd'].value
                ))
        JackHandler.jackConnectAll()

    @staticmethod
    def pdAction(prefix, action, port = 3000): # this is for sending pd functions via a port
        """Sends pd action

        Args:
            prefix (str): The signifing prefx to tell pd what this is
            action (str): the action string
            port (int, optional): The port to send it over. Defaults to 3000.
        """
        command = "echo {} {} \; | pdsend {}".format(prefix, action, port)
        print("PD command: ", command)
        os.system(command)
    
    @staticmethod
    def initPd(effectsDir):
        PdHandler.staticPd = "../Default/"
        JackHandler.init()
        PdHandler.dir = effectsDir
        PdHandler.parseGlobals()
        PdHandler.parseFiles()
