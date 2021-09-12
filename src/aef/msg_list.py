from aitpi import Message

class InputPuredataMessage(Message):
    """Handles input puredata
    """
    msgId = 1001


class PresetMessage(Message):
    """Handles running presets
    """
    msgId = 1002

class RecordingMessage(Message):
    """When the user issues some recording command
    """
    msgId = 1003

class OutputMessage(Message):
    """No data messsages
    """
    msgId = 1004

    def __init__(self, message, type):
        self.message = message
        self.type = type

class EffectsMessage(Message):
    """ Handles effects
    """
    msgId = 1005

