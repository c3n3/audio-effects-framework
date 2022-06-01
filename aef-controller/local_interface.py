import aef
import aitpi
import json
import sys

class LocalInterface():
    """ Handles local aef manipulation
    """
    def init(self):
        """ What happens when a user starts the local app
        """
        effects = "../default_effects/"
        presets = "../default_presets/"
        recordings = "./recordings/"

        aef.run(effects, recordings, presets, sys.argv)
        aitpi.initInput('input.json')

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

    def sync(self):
        """ Syncs the interface with the backend
        """
        pass

    def getCommnds(self):
        """ Gets commands from the backend
        """
        return aef.getCommands()

    def getInputs(self):
        """ Gets inputs from the backend
        """
        f = open('input.json')
        val = json.load(f)
        f.close()
        return val
