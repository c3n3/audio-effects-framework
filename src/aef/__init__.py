from aef.constants import Constants
from aef.effects_handler import EffectsHandler
from aef.global_commands import GlobalCommands
from aef.msg_list import EffectsMessage, PresetMessage, RecordingMessage
from aef.pd_handler import PdHandler
from aef.preset_handler import PresetHandler
from aef.settings import GlobalSettings
from aef.recorder import Recorder
from aitpi.mirrored_json import MirroredJson
import aitpi
import os

_hasRun = False


# Here we must copy over the global pd folder
def ___copyTemps():
    if (not os.path.isfile(GlobalSettings.settings['temp_dir'])):
        os.system("mkdir {} >> {}".format(GlobalSettings.settings['temp_dir'],
            GlobalSettings.settings['temp_dir'] + Constants.SHELL_LOG_FILE))
    os.system("cp {} {} >> {}".format(Constants.GLOBAL_PD, GlobalSettings.settings['temp_dir'],
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

def run(effectsFolder, recordingsFolder, presetsFolder, args=None):
    global _hasRun
    if (not _hasRun):
        GlobalSettings.init(args, effectsFolder, recordingsFolder, presetsFolder)
        ___copyTemps()

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
        aitpi.addRegistry(Constants.DEFAULT_COMMAND_REGISTRY, folderCommands.file)
        
        
        PdHandler.initPd()
        GlobalCommands.init()
        Recorder.init()
        EffectsHandler.init()
        PresetHandler.init()
        _hasRun = True

