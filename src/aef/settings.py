import os
from aef.logger import Logger

class AllSettings():
    """Handles command line arguments
    """
    def __init__(self, settings):
        """Starts settings

        Args:
            settings (TODO): the start settings
        """
        self.settings = settings

    def getAll(self):
        """Gets all settings

        Returns:
            [TODO]: [description]
        """
        return self.settings

    def __getitem__(self, name):
        """Used to get a setting

        Args:
            name (str): The name of the setting

        Returns:
            Setting: the setting
        """
        return self.get(name)

    def __setitem__(self, name, val):
        """Used to set a setting

        Args:
            name (str): The setting
            val (str): The new value
        """
        self.get(name).set(val)

    def get(self, name):
        """Gets a setting

        Args:
            name (str): The settting name

        Returns:
            Setting: The setting
        """
        for s in self.settings:
            if (s.name == name):
                return s
        return None

    def takeArgs(self, args):
        """Takes all the arguments

        Args:
            args (str): a string of the command line arguments
        """
        for i in range(0, len(args)):
            if (args[i].find("-") != -1 and self[args[i].replace('-', '')] != None): # makes sure the args are valid settings
                if (i < len(args) - 1): # if there is another argument for the setting
                    self[args[i].replace('-', '')] = args[i+1]

class Setting():
    """Represents a single Setting
    """
    def __init__(self, name, defautVal, possibleVals):
        self.value = defautVal
        self.name = name
        self.possibleVals = possibleVals

        if (not (defautVal in self.possibleVals) and len(self.possibleVals) != 0):
            self.possibleVals.append(defautVal)

    def set(self, newVal):
        """Sets a setting. Fails if new value not in the list of 'valid' settings

        Args:
            newVal (str): The new value to set
        """
        if (newVal in self.possibleVals):
            self.value = newVal
        elif(len(self.possibleVals) == 0):
            self.value = newVal
        else:
            Logger.log("Invalid value '{}' for '{}'".format(newVal, self.name))
            Logger.log("Keeping original value: '{}'".format(self.value))


class GlobalSettings():
    """Simple class to hold the settings.
       This is what you should use in the future rather than the settings variable.
    """
    settings = AllSettings([
                Setting('debug_pd', 'False', ['True', 'False']),
                Setting('result_pd', '../master.pd', []),
                Setting('global_pd', '../Global/Global.pd', []),
                Setting('scripts_dir', '../Scripts/', []),
                Setting('default_pd', '../Default/Default.pd', []),
            ])

    @staticmethod
    def init():
        """ Inits settings to take arguments

        Args:
            args (string): argv
        """
        import os
        dirname = os.path.dirname(__file__)
        globalPd = os.path.join(dirname, '../../Global')
        reset_pd = os.path.join(dirname, '../../master.pd')
        defaultPd = os.path.join(dirname, '../../Default')
        scripts = os.path.join(dirname, '../../Scripts')
        GlobalSettings.settings['result_pd'] = reset_pd
        GlobalSettings.settings['global_pd'] = globalPd
        GlobalSettings.settings['default_pd'] = defaultPd
        GlobalSettings.settings['scripts_dir'] = scripts

    def __init__(self) -> None:
        raise "Static class"

