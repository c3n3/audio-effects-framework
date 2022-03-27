# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html
from time import sleep
import bluetooth
from commands import *
def receiveMessages():
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)

    client_sock,address = server_sock.accept()
    print ("Accepted connection from " + str(address))

    data = client_sock.recv(1024)
    print ("received [%s]" % data)

    client_sock.close()
    server_sock.close()
  
def sendMessageTo(targetBluetoothMacAddress):
    port = 1
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((targetBluetoothMacAddress, port))
    sock.send("hello!!")
    sock.close()
  
def lookUpNearbyBluetoothDevices():
    nearby_devices = bluetooth.discover_devices()
    l = {}
    for bdaddr in nearby_devices:
        name = str(bluetooth.lookup_name( bdaddr ))
        print (name + " [" + str(bdaddr) + "]")
        l[name] = bdaddr
    return l
devs = lookUpNearbyBluetoothDevices()

name = input("Connect to: ")

port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((devs[name], port))

while (True):
    c = input("Command = ")
    if (c == "c"):
        key = input("Key = ")
        value = input("Value = ")
        sock.send(createChangeCommand(key, value))
    if (c == "g"):
        sock.send(createGetCommands())
        sock.recv(1024).decode()
    if (c == "q"):
        break
sock.close()