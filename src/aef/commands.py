# This class provides a unified way to execute commands
# on the aef system using only json strings.
# This is particulary useful for external control e.g. bluetooth.

import json
from aef.log import *
from aef import msg_list


class Command():
    def __init__(self):
        self.data = {}
        self.type = type(self)
        self.data['type'] = self.type
        self.data['value'] = {}

    def serialize(self):
        return json.dumps(self.data)

    def deserialize(self, data):
        try:
            self.data = json.loads(data)
        except json.JSONDecodeError:
           elog(f"Invalid command json: {data}") 


class AitpiCommand(Command):
    def __init__(self, message):
        super().__init__()
        if not isinstance(message, msg_list):
            wlog("AitpiCommand is only verified to work with 'Message' type and derivitives")
        self.message = message

        for item in dir(self.message):
            if "__" not in item:
                self.data['value'][item] = getattr(self.message, item)
    
    def deserialize(self, data):
        super().deserialize(data)
        ret = msg_list.Message("")
        for attr in self.data['value']:
            setattr(attr, self.data['value'][attr])
        return ret

