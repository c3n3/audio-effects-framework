import os
from time import sleep
from aitpi.postal_service import PostalService
from aef.msg_list import *
from aef.pd_handler import PdHandler
from aef.settings import GlobalSettings

class Recorder():
    """Handles recording files
    """
    state = "IDLE"
    recordingFolder = None
    recordingExt = ".wav"
    recordingCount = 0
    inited = False
    lastPlayed = ""

    @staticmethod
    def save():
        """Saves a new recording from the looper
        """
        if (os.path.isfile('{}loop.wav'.format(GlobalSettings.settings['temp_dir']))):
            # Save loop file
            while (True):
                name = 'Recording_{}{}'.format(Recorder.recordingCount, Recorder.recordingExt)
                file = '{}{}'.format(Recorder.recordingFolder, name)
                Recorder.recordingCount += 1
                if (os.path.isfile(file) == False):
                    break
                
            os.system('cp {}loop.wav {}'.format(GlobalSettings.settings['temp_dir'], file))
            PostalService.sendMessage(OutputMessage("{}\nSaved!".format(name), "NOTIFY"))

    @staticmethod
    def playback(file):
        """Handles playing a recorded file

        Args:
            file (str): The file to actually playback
        """
        Recorder.off()
        if (Recorder.state != "IDLE" and Recorder.lastPlayed == file):
            Recorder.state = "IDLE"
        elif (os.path.isfile(file)):
            Recorder.lastPlayed = file
            copyName = "playback.wav"
            copyFile = "%s%s" % (GlobalSettings.settings['temp_dir'], copyName)
            os.system("cp {} {}".format(file, copyFile))
            sleep(0.1)
            PdHandler.pdAction("global_playback", "open {}, global_playback 1".format(copyName), 3000) # start playback
            Recorder.state = "PLAYING"

    @staticmethod
    def off():
        """Handles shutting of any recording
        """
        PdHandler.pdAction("global_playback", "stop", 3000) # start playback

    @staticmethod
    def consume(msg):
        """Accepts and handles all recorder messages

        Args:
            msg (Message): The message to handle
        """

        # We only care about UP
        if (msg.event == "DOWN"):
            return
        if (msg.name == 'save'):
            Recorder.save()
        else:
            Recorder.playback("{}{}".format(Recorder.recordingFolder, msg.name))

    @staticmethod
    def init():
        Recorder.recordingFolder = GlobalSettings.settings['recordings_dir']
        if (Recorder.inited == False):
            Recorder.inited = True
            PostalService.addConsumer([RecordingMessage.msgId], PostalService.GLOBAL_SUBSCRIPTION, Recorder)
