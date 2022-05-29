from ast import Global
from aef.constants import Constants
from aef.settings import GlobalSettings
name = "{}jack_connect_all.sh".format(Constants.SCRIPTS_DIR)
startingNum = int(GlobalSettings.settings["jack_start_num"])

file = """
until temp=$(jack_connect user_pd:output_1 global_pd:input_1)
do
    echo "Waiting for pd to start"
    sleep 0.1
done
jack_connect user_pd:output_1 global_pd:input_1
jack_connect user_pd:output_2 global_pd:input_2

jack_connect global_pd:output_1 system:playback_1
jack_connect global_pd:output_2 system:playback_2

jack_connect user_pd:output_1 system:playback_1
jack_connect user_pd:output_2 system:playback_2

jack_connect user_pd:input_1 system:capture_1
jack_connect user_pd:input_2 system:capture_1
"""