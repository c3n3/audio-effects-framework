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
from aef.PdRoutingHandler import PdRoutingHandler
import aitpi
import os

from aitpi.postal_service import PostalService

_hasRun = False

# Here we must copy over the global pd folder
def ___copyDefaults():
    # Only create one if we have not made it already, lest we overwite saved data
    if (not os.path.isfile(GS_temp(Constants.TEMP_COMMAND_REG))):
        os.system("cp {} {} >> {}".format(GS_temp(Constants.DEFAULT_COMMAND_REGISTRY),
        GS_temp(Constants.TEMP_COMMAND_REG),
        GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))

def shutdown():
    if (os.system("jack_control status > {}".format(
        GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE)) == 0
        ):
        print("\nClosing now.....")
        from aef.jack_handler import JackHandler
        JackHandler.jackStop()
        from aef.pd_handler import PdHandler
        PdHandler.cleanUpPuredata()
        global _hasRun
        _hasRun = False

def run(effectsFolder, recordingsFolder, presetsFolder, args=None):
    global _hasRun
    if (not _hasRun):
        GlobalSettings.init(args, effectsFolder, recordingsFolder, presetsFolder)
        os.makedirs(GlobalSettings.settings['temp_dir'], exist_ok=True)
        DefaultFiles.init()
        ___copyDefaults()

        folderCommands = MirroredJson(
            os.path.join(
                GlobalSettings.settings['temp_dir'], "foldered_commands.temp.json"))

        folderCommands._settings = []
        
        # Setup recordings
        folderCommands._settings.append({})
        folderCommands[0]['name'] = 'Recordings'
        folderCommands[0]['path'] = recordingsFolder
        folderCommands[0]['type'] = "recordings"
        folderCommands[0]['id'] = RecordingMessage.msgId
        folderCommands[0]['input_type'] = "button"

        # Setup presets
        folderCommands._settings.append({})
        folderCommands[1]['name'] = 'Effects'
        folderCommands[1]["path"] = effectsFolder
        folderCommands[1]["type"] = 'effects'
        folderCommands[1]["id"] = EffectsMessage.msgId
        folderCommands[1]["input_type"] = "button"

        # Setup presets
        folderCommands._settings.append({})
        folderCommands[2]['name'] = 'Presets'
        folderCommands[2]["path"] = presetsFolder
        folderCommands[2]["type"] = 'presets'
        folderCommands[2]["id"] = PresetMessage.msgId
        folderCommands[2]["input_type"] = "button"

        folderCommands.save()
        aitpi.addRegistry(
            GlobalSettings.settings['temp_dir'] +
            Constants.TEMP_COMMAND_REG, folderCommands.file)
        PdHandler.initPd()
        GlobalCommands.init()
        Recorder.init()
        EffectsHandler.init()
        PresetHandler.init()
        PdRoutingHandler.init()

        # Prevent AITPI from spaming prints
        class DummyWatcher():
            def consume(self, msg):
                pass
        aitpi.PostalService.addConsumer(
            [OutputMessage.msgId],
            PostalService.GLOBAL_SUBSCRIPTION,
            DummyWatcher())

        _hasRun = True
