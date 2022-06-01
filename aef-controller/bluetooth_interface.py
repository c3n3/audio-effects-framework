import aef
import aitpi
import sys

class BluetootInterface():
    def init():
        """ What happens when a user starts the app
        """
        pass

    def update(self, key, value):
        """ Code called to update a buttons value

        Args:
            key (string): a valid input
            value (string): A valid command
        """
        pass

    def sync(self):
        """ Syncs the interface with the backend
        """
        pass

    def getCommnds(self):
        """ Gets commands from the backend
        """
        pass

    def getInputs(self):
        """ Gets inputs from the backend
        """
        pass
