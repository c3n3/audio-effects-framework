import os

class Constants():
    SRC_DIR = os.path.dirname(__file__)
    DEFAULT_PD_DIR = 'default/'
    RESULT_PD = "master.pd"
    TOP_PD = "top.pd"
    SCRIPTS_DIR = "scripts/"
    RECORDING_DIR = "recordings/"
    GLOBAL_PD = 'global.pd'
    DEFAULT_COMMAND_REGISTRY = 'default_registry.json'
    TEMP_COMMAND_REG = "command_registry.temp.json"
    SHELL_LOG_FILE = "shell_out.log"
    PD_LOG_FILE = "pd_out.log"
