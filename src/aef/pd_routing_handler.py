import aitpi
from aef.constants import Constants
from aef.msg_list import PdRoutingMessage
from aitpi import router
from aef.pd_handler import PdHandler
from aef.pd_parser import PdParser
from aef.puredata_parser import PuredataFile
from aef.settings import GlobalSettings

class PdRoutingHandler():
    commandRegType = "Puredata Hooks"

    @staticmethod
    def update(hook):
        print("Updating hook")
        PdHandler.pdAction(hook.routeId, hook.current, 2999)

    @staticmethod
    def consume(msg):
        if (msg.name in PdParser.hooks):
            hook = PdParser.hooks[msg.name]
            if (msg.event == "LEFT"):
                hook.down()
            elif (msg.event == "RIGHT"):
                hook.up()
            PdRoutingHandler.update(hook)

    @staticmethod
    def init():
        PdHandler.initHooks()
        router.addConsumer([PdRoutingMessage.msgId], PdRoutingHandler)

        aitpi.clearCommandTypeInRegistry(GlobalSettings.settings['temp_dir'] + Constants.TEMP_COMMAND_REG, PdRoutingHandler.commandRegType)
        for key in PdParser.hooks.keys():
            hook = PdParser.hooks[key]
            aitpi.addCommandToRegistry(GlobalSettings.settings['temp_dir'] + Constants.TEMP_COMMAND_REG,
            hook.name, PdRoutingMessage.msgId, PdRoutingHandler.commandRegType, 'encoder')
