from aef.pd_handler import PdHandler
from aitpi.postal_service import PostalService
from aef.msg_list import EffectsMessage

class EffectsHandler():
    @staticmethod
    def consume(msg):
        if (msg.event == "UP"):
            print("adding: ", msg.name)
            PdHandler.toggleFile(msg.name)
            PdHandler.parseFiles()
    
    @staticmethod
    def init():
        PostalService.addConsumer([EffectsMessage.msgId], PostalService.GLOBAL_SUBSCRIPTION, EffectsHandler)
