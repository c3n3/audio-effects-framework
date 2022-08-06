from aef.constants import Constants

name = Constants.DEFAULT_COMMAND_REGISTRY
file = """
{
    "loop": {
        "type": "Sound recording",
        "input_type": "button",
        "id": "1001"
    },
    "record": {
        "type": "Sound recording",
        "input_type": "button",
        "id": "1001"
    },
    "save": {
        "type": "Sound recording",
        "input_type": "button",
        "id": "1003"
    },
    "volume": {
        "type": "Sound recording",
        "input_type": "encoder",
        "id": "1001"
    }
}
"""
