from aef.pd_handler import PdHandler
from aitpi import router
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
        router.addConsumer([EffectsMessage.msgId], EffectsHandler)
