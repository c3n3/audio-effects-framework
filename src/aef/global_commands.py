from genericpath import isfile
import os
from aitpi.postal_service import PostalService
from aef.msg_list import InputPuredataMessage
from aef.msg_list import OutputMessage
from aef.pd_handler import PdHandler
from time import sleep

class GlobalCommands():
    """Handles sending all global commands

       TODO: Very much later, we will want an arbitrary style global command setup, but it is not needed now.
    """
    isRecording = False
    isPlaying = False
    state = "OFF"
    def __init__(self):
        """Static class
        """
        raise "Static class"

    @staticmethod
    def record():
        """Starts recording audio
        """
        if (not GlobalCommands.isRecording):
            print("Starting this")
            # PdHandler.pdAction(Looper.prefix + "write", "open loop.wav, __looper__write start", 2999) #start record
            PdHandler.pdAction("global_record", "open loop.wav, global_record start", 3000) #start record
            PostalService.sendMessage(OutputMessage('*', "STATUS"))
            GlobalCommands.isRecording = True
        else:
            PdHandler.pdAction("global_record", "stop", 3000) # stop record
            PostalService.sendMessage(OutputMessage(' ', "STATUS"))
            GlobalCommands.isRecording = False
        PostalService.sendMessage(OutputMessage("", "REFRESH"))

    _volume = 80

    @staticmethod
    def volume(leftOrRight):

        PdHandler.pdAction("global_volume", 50, 3000)

    @staticmethod
    def playback():
        """Starts playback of looped audio
        """
        if (GlobalCommands.isRecording):
            # PdHandler.pdAction(Looper.prefix + "write", "stop", 2999) # stop record
            PdHandler.pdAction("global_record", "stop", 3000) # stop record
            PostalService.sendMessage(OutputMessage(' ', "STATUS"))
            PostalService.sendMessage(OutputMessage("", "REFRESH"))
            GlobalCommands.isRecording = False
            sleep(0.1)
            GlobalCommands.playLoop()
        elif (GlobalCommands.isPlaying):
            PdHandler.pdAction("global_loop", "stop", 3000)
            GlobalCommands.isPlaying = False
        else:
            GlobalCommands.playLoop()

    @staticmethod
    def playLoop():
        # TODO: Make the loop.wav location a setting 
        if (os.path.isfile('../Global/loop.wav')):
            PdHandler.pdAction("global_loop", "stop", 3000)
            os.system('cp ../Global/loop.wav ../Global/out.wav') # rename file
            sleep(0.2)
            PdHandler.pdAction("global_loop", "open out.wav, global_loop 1", 3000) # start playback
            GlobalCommands.isPlaying = True
        else:
            print("Cannot find looping file")


    @staticmethod
    def off():
        """Turns playback off
        """
        PdHandler.pdAction("global_loop", "stop", 3000)
        GlobalCommands.isPlaying = False

    @staticmethod
    def consume(msg):
        """Recieves commands to execute

        Args:
            msg (Message):
            To record, send 'record'
            To playback in a loop, send 'playback'
            To change the volume, send 'volume:<0-100>' where of course you change the <...> to a number
        """
        # We do not care if the button is down, just up
        if (msg.event == "DOWN"):
            return
        if (msg.name == 'record'):
            print("Recording")
            GlobalCommands.record()
        elif (msg.name == 'loop'):
            print("Looping")
            GlobalCommands.playback()
        elif (msg.name == 'volume'):
            print("Changing volume")
            GlobalCommands.volume(msg.event)

    @staticmethod
    def init():
        if (not os.path.isfile('../recordings/')):
            os.system("mkdir ../recordings/")
        PostalService.addConsumer([InputPuredataMessage.msgId], PostalService.GLOBAL_SUBSCRIPTION, GlobalCommands)