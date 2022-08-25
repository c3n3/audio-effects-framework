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
from aef.constants import Constants
from aef.default_files import DefaultFiles
from aef.effects_handler import EffectsHandler
from aef.global_commands import GlobalCommands
from aef.msg_list import EffectsMessage, OutputMessage, PresetMessage, RecordingMessage
from aef.pd_handler import PdHandler
from aef.preset_handler import PresetHandler
from aef.settings import GS_temp, GlobalSettings
from aef.recorder import Recorder
from aitpi.mirrored_json import MirroredJson
from aef.pd_routing_handler import PdRoutingHandler
from aef.log import *
from aef import shell
import aitpi
import os

_hasRun = False

# Here we must copy over the global pd folder
def _copyDefaults():
    # Only create one if we have not made it already, lest we overwite saved data
    if not os.path.isfile(GS_temp(Constants.TEMP_COMMAND_REG)):
        shell.run(
            [
                "cp",
                GS_temp(Constants.DEFAULT_COMMAND_REGISTRY),
                GS_temp(Constants.TEMP_COMMAND_REG),
            ]
        )


def getCommands():
    return aitpi.getCommands()


def getInputs():
    return aitpi.getInputs()


def shutdown():
    ilog("Closing now.....")
    from aef.jack_handler import JackHandler
    JackHandler.jackStop()
    from aef.pd_handler import PdHandler
    PdHandler.cleanUpPuredata()
    global _hasRun
    _hasRun = False


def run(effectsFolder, recordingsFolder, presetsFolder, args=None):
    global _hasRun
    if not _hasRun:
        GlobalSettings.init(args, effectsFolder, recordingsFolder, presetsFolder)
        os.makedirs(GlobalSettings.settings["temp_dir"], exist_ok=True)
        DefaultFiles.init()
        _copyDefaults()

        folderCommands = MirroredJson(
            os.path.join(
                GlobalSettings.settings["temp_dir"], "foldered_commands.temp.json"
            )
        )

        folderCommands._settings = []

        # Setup recordings
        folderCommands._settings.append({})
        folderCommands[0]["name"] = "Recordings"
        folderCommands[0]["path"] = recordingsFolder
        folderCommands[0]["type"] = "recordings"
        folderCommands[0]["id"] = RecordingMessage.msgId
        folderCommands[0]["input_type"] = "button"

        # Setup effects
        folderCommands._settings.append({})
        folderCommands[1]["name"] = "Effects"
        folderCommands[1]["path"] = effectsFolder
        folderCommands[1]["type"] = "effects"
        folderCommands[1]["id"] = EffectsMessage.msgId
        folderCommands[1]["input_type"] = "button"

        # Setup presets
        folderCommands._settings.append({})
        folderCommands[2]["name"] = "Presets"
        folderCommands[2]["path"] = presetsFolder
        folderCommands[2]["type"] = "presets"
        folderCommands[2]["id"] = PresetMessage.msgId
        folderCommands[2]["input_type"] = "button"

        folderCommands.save()
        aitpi.addRegistry(
            GlobalSettings.settings["temp_dir"] + Constants.TEMP_COMMAND_REG,
            folderCommands.file,
        )
        PdHandler.initPd()
        GlobalCommands.init()
        Recorder.init()
        EffectsHandler.init()
        PresetHandler.init()
        PdRoutingHandler.init()

        # Prevent AITPI from spaming prints
        class DummyWatcher:
            def consume(self, msg):
                pass

        aitpi.router.addConsumer([OutputMessage.msgId], DummyWatcher())

        _hasRun = True


def changeLink(inputName, newRegLink):
    print("Changing link")
    aitpi.changeInputRegLink(inputName, newRegLink)
