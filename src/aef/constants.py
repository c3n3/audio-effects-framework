import os

class Constants():
    SRC_DIR = os.path.dirname(__file__)
    DEFAULT_PD_DIR = os.path.join(SRC_DIR, '../../Default/')
    RESULT_PD = "master.pd"
    SCRIPTS_DIR = os.path.join(SRC_DIR, "../../Scripts/")
    GLOBAL_PD = os.path.join(SRC_DIR, '../../Global/Global.pd')
    DEFAULT_COMMAND_REGISTRY = os.path.join(SRC_DIR, '../../default_registry.json')
    TEMP_COMMAND_REG = "command_registry.temp.json"
    SHELL_LOG_FILE = "shell_out.log"
    PD_LOG_FILE = "pd_out.log"
