from aef.pd_handler import PdHandler
from aitpi import router
from aef.msg_list import EffectsMessage
from aef.pd_parser import PdParser
from aef.pd_routing_handler import PdRoutingHandler

class EffectsHandler():
    @staticmethod
    def consume(msg):
        if (msg.event == "UP"):
            print("adding: ", msg.name)
            for hook in PdParser.filesToHooks[msg.name].keys():
                PdRoutingHandler.update(hook)
            PdHandler.toggleFile(msg.name)
            PdHandler.parseFiles()

    @staticmethod
    def init():
        router.addConsumer([EffectsMessage.msgId], EffectsHandler)
