import aef
import os
print("TEST")

try:
    aef.run(None)
except KeyboardInterrupt:
    if (os.system("jack_control status > /dev/null") == 0):
        print("\nClosing now.....")
        from aef.jack_handler import JackHandler
        JackHandler.jackStop()
        from aef.pd_handler import PdHandler
        PdHandler.cleanUpPuredata()
