# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
#
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html
import time
import bluetooth
from commands import *
from aef import commands

class BluetoothServer():
    devices = {}

    def __init__(self):
        self.commands = {}
        self.port = 1
        self.sock = None

    def connect(self, addr):
        if (self.sock):
            self.sock.close()
        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        print("Connecting", addr, self.port, self.sock)
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

    def send(self, command):
        got = ""
        self.sock.send(command.serialize())
        start = time.time()
        while (True):
            if (time.time() - start > 5):
                print("Error json is bad")
                break
            got += self.sock.recv(1000).decode()
            try:
                ret = json.loads(got)
                return ret
            except json.JSONDecodeError:
                print("Invalid json")

if __name__ == "__main__":
    BluetoothServer.lookUpNearbyBluetoothDevices()

    server = BluetoothServer()
    server.connect(input("Addr: "))
    com = commands.GetCommands()
    print("Got", server.send(com))