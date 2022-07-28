from time import sleep
from aef.pd_handler import PdHandler
from aitpi import router
from aef.msg_list import EffectsMessage
from aef.pd_parser import PdParser
from aef.pd_routing_handler import PdRoutingHandler

class EffectsHandler():
    @staticmethod
    def consume(msg):
        if (msg.event == "0"):
            PdHandler.toggleFile(msg.name)
            PdHandler.parseFiles()
            if msg.name in PdParser.filesToHooks:
                print("Re init hook")
                sleep(0.2)
                for hook in PdParser.filesToHooks[msg.name]:
                    print("Re init hook p2")
                    PdRoutingHandler.update(hook)

    @staticmethod
    def init():
        router.addConsumer([EffectsMessage.msgId], EffectsHandler)
