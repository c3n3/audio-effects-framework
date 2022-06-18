import aitpi
from aef.constants import Constants
from aef.msg_list import PdRoutingMessage
from aitpi.postal_service import PostalService
from aef.pd_handler import PdHandler
from aef.puredata_parser import PuredataFile
from aef.settings import GlobalSettings

class PdRoutingHandler():
    commandRegType = "Puredata Hooks"
    @staticmethod
    def consume(msg):
        for hook in PuredataFile.routingHooks:
            if (hook.name == msg.name):
                if (msg.event == "LEFT"):
                    hook.down()
                elif (msg.event == "RIGHT"):
                    hook.up()
                PdHandler.pdAction(hook.routeId, hook.current, 2999)
                break

    @staticmethod
    def init():
        PdHandler.initHooks()
        PostalService.addConsumer([PdRoutingMessage.msgId], PostalService.GLOBAL_SUBSCRIPTION, PdRoutingHandler)

        aitpi.clearCommandTypeInRegistry(GlobalSettings.settings['temp_dir'] + Constants.TEMP_COMMAND_REG, PdRoutingHandler.commandRegType)
        for hook in PuredataFile.routingHooks:
            aitpi.addCommandToRegistry(GlobalSettings.settings['temp_dir'] + Constants.TEMP_COMMAND_REG,
            hook.name, PdRoutingMessage.msgId, PdRoutingHandler.commandRegType, 'encoder')
