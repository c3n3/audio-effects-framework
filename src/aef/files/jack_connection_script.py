from aef.constants import Constants
name = "{}jack_connect_all.sh".format(Constants.SCRIPTS_DIR)
file = """
until temp=$(jack_connect user_pd:output0 global_pd:input0)
do
    echo "Waiting for pd to start"
    sleep 0.1
done
jack_connect user_pd:output0 global_pd:input0
jack_connect user_pd:output1 global_pd:input1

jack_connect global_pd:output0 system:playback_1
jack_connect global_pd:output1 system:playback_2

jack_connect user_pd:output0 system:playback_1
jack_connect user_pd:output1 system:playback_2

jack_connect user_pd:input0 system:capture_1
jack_connect user_pd:input1 system:capture_1
"""