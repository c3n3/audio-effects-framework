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

validCommands = {"ChangeLink": ChangeLink, "AitpiMsg": AitpiMsg, "GetCommands": GetCommands}

def handleCommand(string):
    data = json.loads(string)
    if 'type' in data and data['type'] in validCommands:
        command = validCommands[data['type']]()
        command.setData(data)
        command.execute()
        return command.response()
    else:
        elog("Invalid command", string)
