import aef
import aitpi
import json
import sys
from interface import AefInterface

class LocalInterface(AefInterface):
    """ Handles local aef manipulation
    """
    def init(self):
        """ What happens when a user starts the local app
        """
        effects = "../default_effects/"
        presets = "../default_presets/"
        recordings = "../recordings/"

        aef.run(effects, recordings, presets, sys.argv)
        aitpi.initInput('../example_input.json')

    def close(self):
        """ Close the interface
        """
        aef.shutdown()

    def update(self, key, value):
        """ Code called to update a buttons value

        Args:
            key (string): a valid input
            value (string): A valid command
        """
        aef.changeLink(key, value)

    def getCommnds(self):
        """ Gets commands from the backend
        """
        return aef.getCommands()

    def getInputs(self):
        """ Gets inputs from the backend
        """
        return aef.getInputs()
