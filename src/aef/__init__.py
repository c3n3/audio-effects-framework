from aef.global_commands import GlobalCommands
from aef.pd_handler import PdHandler
from aef.settings import GlobalSettings
from aef.recorder import Recorder
import aitpi
import os

_hasRun = False

def run(folders=None):
    global _hasRun
    if (not _hasRun):
        dirname = os.path.dirname(__file__)
        folderCommands = os.path.join(dirname, '../../folders.json') if folders == None else folders
        defReg = os.path.join(dirname, '../../default_registry.json')
        aitpi.addRegistry(defReg, folderCommands)
        GlobalSettings.init()
        PdHandler.initPd("../temp/")
        GlobalCommands.init()
        Recorder.init()
        _hasRun = True

