import aef
import sys
import os
import aitpi
from aitpi.postal_service import PostalService

class OutputWatch():
    def consume(self, msg):
        print("Msg: %s, Type: %s" % (msg.message, msg.type))

try:
    dirname = os.path.dirname(__file__)
    recordingsFolder = os.path.join(dirname, '../../recordings/')
    effectsFolder = os.path.join(dirname, '../../default_effects/')
    presetsFolder = os.path.join(dirname, '../../default_presets/')
    aef.run(effectsFolder, recordingsFolder, presetsFolder, sys.argv)
    inputJson = os.path.join(dirname, '../../example_input.json')
    aitpi.initInput(inputJson)
    PostalService.addConsumer([1004], PostalService.GLOBAL_SUBSCRIPTION, OutputWatch())
    while (True):
        aitpi.takeInput(input("Input: "))
except KeyboardInterrupt:
    aef.shutdown()

