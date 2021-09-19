from aef.msg_list import PresetMessage
from aitpi.postal_service import PostalService
from aef.pd_handler import PdHandler

class PresetHandler():
    @staticmethod
    def consume(msg):
        """Handles actually running the preset commands that are sent through the CentralRouter

        Args:
            msg (Message): Message containing the preset to run
        """
        if (msg.event == "DOWN"):
            return
        f = open(msg.attributes['path'] + msg.name, "r")
        lines = f.readlines()
        PdHandler.files = []
        for i in range(0, len(lines)):
            PdHandler.toggleFile(lines[i].replace('\n', ''))
        PdHandler.parseFiles()

    @staticmethod
    def init():
        PostalService.addConsumer([PresetMessage.msgId], PostalService.GLOBAL_SUBSCRIPTION, PresetHandler)