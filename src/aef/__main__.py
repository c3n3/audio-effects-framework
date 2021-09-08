import aef
import os
import aitpi
from aitpi.postal_service import PostalService
print("TEST")

class OutputWatch():
    def consume(self, msg):
        print("Msg: %s, Type: %s" % (msg.message, msg.type))

try:
    dirname = os.path.dirname(__file__)
    folderCommands = os.path.join(dirname, '../../folders.json')
    aef.run(folderCommands)
    inputJson = os.path.join(dirname, '../../example_input.json')
    aitpi.initInput(inputJson)
    PostalService.addConsumer([1004], PostalService.GLOBAL_SUBSCRIPTION, OutputWatch())
    while (True):
        aitpi.takeInput(input("Input: "))
except KeyboardInterrupt:
    if (os.system("jack_control status > /dev/null") == 0):
        print("\nClosing now.....")
        from aef.jack_handler import JackHandler
        JackHandler.jackStop()
        from aef.pd_handler import PdHandler
        PdHandler.cleanUpPuredata()
