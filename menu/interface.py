import aef
import aitpi
import sys

class AefInterface():
    interface = None

    """ Handles local aef manipulation
    """
    def init(self):
        """ What happens when a user starts the local app
        """
        pass

    def close(self):
        """ Close the interface
        """
        pass

    def update(self, key, value):
        """ Code called to update an inputs value

        Args:
            key (string): a valid input
            value (string): A valid command
        """
        pass

    def getCommnds(self):
        """ Gets commands from the backend
        """
        pass

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
        pass
