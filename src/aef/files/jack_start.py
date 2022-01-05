from aef.constants import Constants
name = "{}jack_start.sh".format(Constants.SCRIPTS_DIR)
file = """
jack_control start
jack_control ds alsa
jack_control dps device hw:sndrpihifiberry
jack_control dps rate 48000
jack_control dps period 64
"""
