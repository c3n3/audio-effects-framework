import aef
import sys
import os
import aitpi
from aitpi import router
from aef.pd_parser import PdParser
from aef.log import *
from aef import shell
from aef import blutooth_control
import time

from aef import commands
from aef.msg_list import Message

class OutputWatch:
    def consume(self, msg):
        print("Msg: %s, Type: %s" % (msg.message, msg.type))

try:
    dirname = os.path.dirname(__file__)
    recordingsFolder = os.path.join(dirname, "../../recordings/")
    effectsFolder = os.path.join(dirname, "../../default_effects/")
    presetsFolder = os.path.join(dirname, "../../default_presets/")
    aef.run(effectsFolder, recordingsFolder, presetsFolder, sys.argv)
    inputJson = os.path.join(dirname, "../../example_input.json")
    aitpi.initInput(inputJson)
    router.addConsumer([1004], OutputWatch())

    if GlobalSettings.settings["bluetooth"] == "True":
        blutooth_control.run()
    else:
        while True:
            aitpi.takeInput(input("Input: "))
except KeyboardInterrupt:
    pass
finally:
    pass
    aef.shutdown()
