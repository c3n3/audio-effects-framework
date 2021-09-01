class Logger():
    """The logger class. Used to log any usefull messages.
       Use this instead of print in ALL cases
    """
    def __init__(self):
        """NO init for you
        """
        raise "Static class"

    @staticmethod
    def log(msg, SEVERITY="NOTE"):
        """Simple logging of message

        Args:
            msg (str): Message to log
        """
        print(msg)

    @staticmethod
    def notify(msg):
        """TODO: Notify? Should remove and make log of a severity argument
        """
        if (settings['instance'] != 'pi'):
            print(msg)
