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

    def sync(self):
        """ Syncs the interface with the backend
        """
        pass

    def getCommnds(self):
        """ Gets commands from the backend
        """
        return aef.getCommands()

    def getInputsByType(self, type):
        inputs = self.getInputs()

        ret = []
        for input in inputs:
            if input['type'] == type:
                ret.append(input)
        return ret

    def getCommandsByInputType(self, inType):
        commands = self.getCommnds()

        ret = []
        for command in commands:
            if command['input_type'] == inType:
                ret.append(command)
        return ret

    def getInputs(self):
        """ Gets inputs from the backend
        """
        return aef.getInputs()
