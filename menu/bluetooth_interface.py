import time
import bluetooth
from aef import commands
import json
from aef.msg_list import *
from aef.log import *

class BluetoothServer():
    devices = {}

    def __init__(self):
        self.commands = {}
        self.port = 1
        self.sock = None
        self.connected = False

    def connect(self, addr):
        if (self.sock):
            self.sock.close()
        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        try:
            self.sock.connect((addr, self.port))
            self.connected = True
        except:
            self.connected = False

    def isConnected(self):
        if self.connected:
            com = commands.Ping()
            try:
                val = self.send(com)
                if val['value'] == True:
                    self.connected = True
            except:
                self.connected = False
        return self.connected

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
                pass


class BluetootInterface():
    def init(self):
        """ What happens when a user starts the app
        """
        self.server = BluetoothServer()

    def connectTo(self, addr):
        self.server.connect(addr)
        return self.server.isConnected()

    def getFoundDevices(self):
        return BluetoothServer.devices

    def searchForDevices(self):
        BluetoothServer.lookUpNearbyBluetoothDevices()

    def update(self, key, value):
        """ Code called to update a buttons value

        Args:
            key (string): a valid input
            value (string): A valid command
        """
        com = commands.ChangeLink()
        com.use(key, value)
        self.server.send(com)

    def getCommnds(self):
        """ Gets commands from the backend
        """
        com = commands.GetCommands()
        return self.server.send(com)

    def getInputs(self):
        """ Gets inputs from the backend
        """
        com = commands.GetInputs()
        return self.server.send(com)
