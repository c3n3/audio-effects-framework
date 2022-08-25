# Audio Effects Framework - A python library to setup Puredata effects
# Copyright (C) 2022  Caden Churchman
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os


class AllSettings:
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
        res = self.get(name)
        if res == None:
            return None
        return res.value

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
            if s.name == name:
                return s
        return None

    def takeArgs(self, args):
        """Takes all the arguments

        Args:
            args (str): a string of the command line arguments
        """
        if args == None:
            return
        for i in range(0, len(args)):
            if (
                args[i].find("-") != -1 and self[args[i].replace("-", "")] != None
            ):  # makes sure the args are valid settings
                if i < len(args) - 1:  # if there is another argument for the setting
                    self[args[i].replace("-", "")] = args[i + 1]


class Setting:
    """Represents a single Setting
    """

    def __init__(self, name, defautVal, possibleVals):
        self.value = defautVal
        self.name = name
        self.possibleVals = possibleVals

        if not (defautVal in self.possibleVals) and len(self.possibleVals) != 0:
            self.possibleVals.append(defautVal)

    def set(self, newVal):
        """Sets a setting. Fails if new value not in the list of 'valid' settings

        Args:
            newVal (str): The new value to set
        """
        if newVal in self.possibleVals:
            self.value = newVal
        elif len(self.possibleVals) == 0:
            self.value = newVal
        else:
            # TODO: Cannot use log here since log depends on settings, maybe a better way for this
            print("AEF::ARGS: Invalid value '{}' for '{}'".format(newVal, self.name))
            print("AEF::ARGS: Keeping original value: '{}'".format(self.value))


class GlobalSettings:
    """Simple class to hold the settings.
       This is what you should use in the future rather than the settings variable.
    """

    settings = AllSettings(
        [
            Setting("debug_pd", "False", ["True", "False"]),
            Setting("recordings_dir", "", []),
            Setting("scale_volume", "5", []),
            Setting("log_folder", "", []),
            Setting("log_level", "Debug", ["Debug", "Info", "Warning", "Error"]),
            Setting("log_level", "Debug", ["Debug", "Info", "Warning", "Error"]),
            Setting("presets_dir", "", []),
            Setting("effects_dir", "", []),
            Setting("bluetooth", "False", ["True", "False"]),
            Setting("temp_dir", "./temp/", []),
            Setting("jackdrc", f"{os.getenv('HOME')}/.jackdrc", []),
        ]
    )

    @staticmethod
    def init(args, effects, recordings, presets):
        """ Inits settings to take arguments

        Args:
            args (string): argv
        """
        # GlobalSettings.settings['result_pd'] = reset_pd
        GlobalSettings.settings["effects_dir"] = effects
        GlobalSettings.settings["presets_dir"] = presets
        GlobalSettings.settings["recordings_dir"] = recordings
        GlobalSettings.settings.takeArgs(args)

    def __init__(self) -> None:
        raise "Static class"


def GS_temp(name):
    return GlobalSettings.settings["temp_dir"] + name
