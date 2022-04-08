# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

from commands import *

import aef
import sys
import aitpi
from time import sleep
import bluetooth

class BlueToothHandler():
    def __init__(self):
        self.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.port = 1
        self.server_sock.bind(("",self.port))
        self.server_sock.listen(1)
        print("Waiting for connection...")
        client_sock,address = self.server_sock.accept()
        self.cli = client_sock
        self.addr = address
        print ("Accepted connection from " + str(address))

    def listen(self):
        data = json.loads(self.cli.recv(1024).decode())
        self.executeCommand(data)

    def executeCommand(self, val):
        if (val["command"] == GET_COMMANDS_COMMAND):
            print("Test")
            vals = createReturnCommands(aef.getCommands())
            print("sending", vals)
            self.send(vals)
        if (val["command"] == CHANGE_COMMAND):
            print("Changing", val["key"], "to", val["value"])
            aef.changeLink(val["key"], val["value"])

    def close(self):
        self.cli.close()
        self.server_sock.close()


    def send(self, string):
        for i in range((len(string) // 1000) + 1):
            end = (i+1) * 1000
            if (end > len(string)):
                end = len(string)
            send = string[i*1000:end]
            self.cli.send(send)

effects = "../default_effects/"
presets = "../default_presets/"
recordings = "./recordings/"

def init():
    print("args", sys.argv)
    aef.run(effects, recordings, presets, sys.argv)

init()
aitpi.initInput('rpi_v3_input.json')

while (True):
    blue = None
    try:
        blue = BlueToothHandler()
        while (True):
            blue.listen()
    except KeyboardInterrupt:
        print("Keyboard shutdown")
        if (blue != None):
            blue.close()
        exit()
    except Exception as e:
        print(str(e))
        if (blue != None):
            blue.close()
    print("Dropped connection, waiting...")
    sleep(5)

aef.shutdown()
