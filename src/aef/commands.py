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

# This class provides a unified way to execute commands
# on the aef system using only json strings.
# This is particulary useful for external control e.g. bluetooth.

import json
from aef.log import *
from aef import msg_list
import aef
from aitpi import router

class Command():
    def __init__(self):
        self.data = {}
        self.type = type(self).__name__
        self.data['type'] = self.type
        self.data['value'] = {}

    def serialize(self):
        return json.dumps(self.data)

    def setData(self, data):
        self.data = data

    def execute(self):
        pass

    def response(self):
        return None

class ChangeLink(Command):
    def use(self, inputName, newRegLink):
        self.data['value']['name'] = inputName
        self.data['value']['link'] = newRegLink

    def execute(self):
        aef.changeLink(self.data['value']['name'], self.data['value']['link'])


class GetCommands(Command):
    def response(self):
        return aef.getCommands()


class GetInputs(Command):
    def response(self):
        return aef.getInputs()


class Ping(Command):
    def response(self):
        return {'value': True}


class AitpiMsg(Command):
    def use(self, message):
        super().__init__()
        if not isinstance(message, msg_list.Message):
            wlog("AitpiCommand is only verified to work with 'Message' type and derivitives")
        self.message = message

        for item in dir(self.message):
            if "__" not in item:
                self.data['value'][item] = getattr(self.message, item)

    def getMsg(self):
        ret = msg_list.Message("")
        for attr in self.data['value']:
            setattr(ret, attr, self.data['value'][attr])
        return ret

    def execute(self):
        router.send(self.getMsg())

validCommands = {"ChangeLink": ChangeLink, "AitpiMsg": AitpiMsg, "GetCommands": GetCommands, "Ping": Ping, "GetInputs": GetInputs}

def handleCommand(string):
    data = json.loads(string)
    if 'type' in data and data['type'] in validCommands:
        command = validCommands[data['type']]()
        command.setData(data)
        command.execute()
        return command.response()
    else:
        elog("Invalid command", string)
