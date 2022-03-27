# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html
from time import sleep
import bluetooth
from commands import *

class BluetoothServer():
    devices = {}

    def __init__(self):
        self.commands = {}
        self.port = 1
        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    def connect(self, addr):
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
        self.sock.send(createGetCommands())
        self.commands = json.loads(self.sock.recv(4048).decode())

    def close(self):
        self.sock.close()
