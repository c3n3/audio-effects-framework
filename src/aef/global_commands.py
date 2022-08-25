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

from genericpath import isfile
import os
from aitpi import router
from aef.constants import Constants
from aef.msg_list import InputPuredataMessage
from aef.msg_list import OutputMessage
from aef.pd_handler import PdHandler
from time import sleep
from aef.log import *
from aef.settings import GlobalSettings
from aef import shell


class GlobalCommands:
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
        if not GlobalCommands.isRecording:
            # PdHandler.pdAction(Looper.prefix + "write", "open loop.wav, __looper__write start", 2999) #start record
            PdHandler.pdAction(
                "global_record", "open loop.wav, global_record start", 3000
            )  # start record
            router.sendMessage(OutputMessage(["*", "STATUS"]))
            GlobalCommands.isRecording = True
        else:
            PdHandler.pdAction("global_record", "stop", 3000)  # stop record
            router.sendMessage(OutputMessage([" ", "STATUS"]))
            GlobalCommands.isRecording = False
        router.sendMessage(OutputMessage(["", "REFRESH"]))

    _volume = 80

    @staticmethod
    def volume(leftOrRight):
        if leftOrRight == "LEFT":
            GlobalCommands._volume = (
                GlobalCommands._volume - 5 if GlobalCommands._volume != 0 else 0
            )
        elif leftOrRight == "RIGHT":
            GlobalCommands._volume = (
                GlobalCommands._volume + 5 if GlobalCommands._volume != 400 else 400
            )
        PdHandler.pdAction("__default__volume", GlobalCommands._volume / 100, 2999)

    @staticmethod
    def playback():
        """Starts playback of looped audio
        """
        if GlobalCommands.isRecording:
            # PdHandler.pdAction(Looper.prefix + "write", "stop", 2999) # stop record
            PdHandler.pdAction("global_record", "stop", 3000)  # stop record
            router.sendMessage(OutputMessage([" ", "STATUS"]))
            router.sendMessage(OutputMessage(["", "REFRESH"]))
            GlobalCommands.isRecording = False
            sleep(0.1)
            GlobalCommands.playLoop()
        elif GlobalCommands.isPlaying:
            PdHandler.pdAction("global_loop", "stop", 3000)
            GlobalCommands.isPlaying = False
        else:
            GlobalCommands.playLoop()

    @staticmethod
    def playLoop():
        # TODO: Make the loop.wav location a setting
        if os.path.isfile("{}loop.wav".format(GlobalSettings.settings["temp_dir"])):
            PdHandler.pdAction("global_loop", "stop", 3000)
            shell.run(
                [
                    "cp",
                    "{}loop.wav".format(GlobalSettings.settings["temp_dir"]),
                    "{}out.wav".format(GlobalSettings.settings["temp_dir"]),
                ]
            )
            sleep(0.2)
            PdHandler.pdAction(
                "global_loop", "open out.wav, global_loop 1", 3000
            )  # start playback
            GlobalCommands.isPlaying = True
        else:
            elog("Cannot find looping file")

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
        if msg.event == "1":
            return
        if msg.name == "record":
            GlobalCommands.record()
        elif msg.name == "loop":
            GlobalCommands.playback()
        elif msg.name == "volume":
            GlobalCommands.volume(msg.event)

    @staticmethod
    def init():
        router.addConsumer([InputPuredataMessage.msgId], GlobalCommands)
