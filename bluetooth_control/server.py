# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html
import time
import bluetooth
from commands import *

class BluetoothServer():
    devices = {}

    def __init__(self):
        self.commands = {}
        self.port = 1
        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    def connect(self, addr):
        self.close()
        self.sock.connect((addr, self.port))

    @staticmethod
    def lookUpNearbyBluetoothDevices():
        nearby_devices = bluetooth.discover_devices()
        l = {}
        for bdaddr in nearby_devices:
            name = str(bluetooth.lookup_name( bdaddr ))
            print (name + " [" + str(bdaddr) + "]")
            l[name] = bdaddr
        BluetoothServer.devices = l

    def updateCommand(self, key, value):
        self.sock.send(createChangeCommand(key, value))

    def sync(self):
        got = ""
        self.sock.send(createGetCommands())
        start = time.time()
        while (True):
            if (time.time() - start > 5):
                print("Error json is bad")
                break
            got += self.sock.recv(1000).decode()
            try:
                self.commands = json.loads(got)["values"]
                break
            except:
                print("Invalid json")

    def close(self):
        self.sock.close()
