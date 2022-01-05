from aef.constants import Constants
name = "{}jack_disconnect_all.sh".format(Constants.SCRIPTS_DIR)
file = """
jack_disconnect user_pd:output0 global_pd:input_1
jack_disconnect user_pd:output1 global_pd:input_2
"""
