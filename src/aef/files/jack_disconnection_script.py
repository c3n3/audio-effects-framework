from aef.constants import Constants
from aef.settings import GlobalSettings

name = "{}jack_disconnect_all.sh".format(Constants.SCRIPTS_DIR)
startingNum = int(GlobalSettings.settings["jack_start_num"])

file = """
jack_disconnect user_pd:output0 global_pd:input{}
jack_disconnect user_pd:output1 global_pd:input{}
""".format(startingNum, startingNum + 1)
