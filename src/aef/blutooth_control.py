# Audio Effects Framework - A python library to setup Puredata effects
# Copyright (C) 2022  Caden Churchman
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
#
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

from time import sleep
import bluetooth
from aef.log import *
import json
from aef.commands import handleCommand

class BlueToothHandler():
    def __init__(self):
        self.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.port = 1
        self.server_sock.bind(("",self.port))
        self.server_sock.listen(1)
        self.cli = None
    
    def waitForConnect(self):
        ilog("Waiting for connection...")
        client_sock,address = self.server_sock.accept()
        self.cli = client_sock
        self.addr = address
        ilog ("Accepted connection from " + str(address))

    def listen(self):
        send = handleCommand(self.cli.recv(1024).decode())
        self.send(json.dumps(send))

    def close(self):
        if self.cli:
            self.cli.close()
        self.server_sock.close()

    def send(self, string):
        for i in range((len(string) // 1000) + 1):
            end = (i+1) * 1000
            if (end > len(string)):
                end = len(string)
            send = string[i*1000:end]
            self.cli.send(send)

def run():
    while (True):
        blue = None
        try:
            blue = BlueToothHandler()
            blue.waitForConnect()
            while (True):
                blue.listen()
        except KeyboardInterrupt:
            if (blue != None):
                blue.close()
            break
        except Exception as e:
            print(str(e))
            if (blue != None):
                blue.close()
        ilog("Dropped connection, waiting...")
        sleep(1)

