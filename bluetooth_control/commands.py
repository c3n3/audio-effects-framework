import json

CHANGE_COMMAND = "CHANGE"
def createChangeCommand(key, value):
    return json.dumps({"command": CHANGE_COMMAND, "key": key, "value": value})

GET_COMMANDS_COMMAND = "GET_COMMANDS"
def createGetCommands():
    return json.dumps({"command": GET_COMMANDS_COMMAND})

RETURN_COMMANDS_COMMAND = "RETURN_COMMANDS"
def createReturnCommands(values):
    return json.dumps({"command": RETURN_COMMANDS_COMMAND, "values": values})

def parse(string):
    return json.loads(string)
