from aef.global_commands import GlobalCommands
from aef.pd_handler import PdHandler
from aef.settings import GlobalSettings
import aitpi
import os

_hasRun = False

def run(folders):
    global _hasRun
    if (not _hasRun):
        dirname = os.path.dirname(__file__)
        defReg = os.path.join(dirname, '../../default_registry.json')
        aitpi.addRegistry(defReg, folders)
        GlobalSettings.init()
        PdHandler.initPd("../temp/")
        GlobalCommands.init()
        _hasRun = True

