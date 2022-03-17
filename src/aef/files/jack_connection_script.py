from ast import Global
from aef.constants import Constants
from aef.settings import GlobalSettings
name = "{}jack_connect_all.sh".format(Constants.SCRIPTS_DIR)
startingNum = int(GlobalSettings.settings["jack_start_num"])

file = """
until temp=$(jack_connect user_pd:output_{} global_pd:input_{})
do
    echo "Waiting for pd to start"
    sleep 0.1
done
jack_connect user_pd:output_{} global_pd:input_{}
jack_connect user_pd:output_{} global_pd:input_{}

jack_connect global_pd:output_{} system:playback_1
jack_connect global_pd:output_{} system:playback_2

jack_connect user_pd:output_{} system:playback_1
jack_connect user_pd:output_{} system:playback_2

jack_connect user_pd:input_{} system:capture_1
jack_connect user_pd:input_{} system:capture_1
""".format(
    startingNum, startingNum,
    startingNum, startingNum,
    startingNum+1, startingNum+1,

    startingNum, startingNum+1,
    startingNum, startingNum+1,
    startingNum, startingNum+1,
)
