# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

from commands import *
import aef
from time import sleep
import bluetooth

# def receiveMessages():
#     server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

#     port = 1
#     server_sock.bind(("",port))
#     server_sock.listen(1)

#     client_sock,address = server_sock.accept()
#     print ("Accepted connection from " + str(address))

#     data = client_sock.recv(1024)
#     print ("received [%s]" % data)

#     client_sock.close()
#     server_sock.close()
  
# def sendMessageTo(targetBluetoothMacAddress):
#     port = 1
#     sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#     sock.connect((targetBluetoothMacAddress, port))
#     sock.send("hello!!")
#     sock.close()
  
# def lookUpNearbyBluetoothDevices():
#     nearby_devices = bluetooth.discover_devices()
#     l = {}
#     for bdaddr in nearby_devices:
#         name = str(bluetooth.lookup_name( bdaddr ))
#         print (name + " [" + str(bdaddr) + "]")
#         l[name] = bdaddr
#     return l


class BlueToothHandler():
    def __init__(self):
        self.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.port = 1
        self.server_sock.bind(("",self.port))
        self.server_sock.listen(1)
        client_sock,address = self.server_sock.accept()
        self.cli = client_sock
        self.addr = address
        print ("Accepted connection from " + str(address))

    def listen(self):
        data = json.loads(self.cli.recv(1024).decode())
        self.executeCommand(data)

    def executeCommand(self, val):
        if (val["command"] == GET_COMMANDS_COMMAND):
            self.cli.send(createReturnCommands(aef.getCommands()))
        if (val["command"] == CHANGE_COMMAND):
            print("Changing", val["key"], "to", val["value"])
            #aef.changeLink(val["key"], val["value"])

    def __del__(self):
        self.cli.close()
        self.server_sock.close()

while (True):
    blue = BlueToothHandler()
    try:
        while (True):
            blue.listen()
    except:
        pass
    print("Dropped connection, waiting...")
    sleep(5)