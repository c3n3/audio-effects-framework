from time import sleep
from aef.pd_handler import PdHandler
from aitpi import router
from aef.msg_list import EffectsMessage
from aef.pd_parser import PdParser
from aef.pd_routing_handler import PdRoutingHandler
from aef.log import *


class EffectsHandler:
    @staticmethod
    def consume(msg):
        if msg.event == "0":
            PdHandler.toggleFile(msg.name)
            PdHandler.parseFiles()
            if msg.name in PdParser.filesToHooks:
                dlog("Re-init hooks for", msg.name)
                sleep(0.2)
                for hook in PdParser.filesToHooks[msg.name]:
                    PdRoutingHandler.update(hook)

    @staticmethod
    def init():
        router.addConsumer([EffectsMessage.msgId], EffectsHandler)
