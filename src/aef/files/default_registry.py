from aef.constants import Constants

name = Constants.DEFAULT_COMMAND_REGISTRY
file = """
{
    "sound recording": {
        "loop": {
            "input_type": "button",
            "id": "1001"
        },
        "record": {
            "input_type": "button",
            "id": "1001"
        },
        "save": {
            "input_type": "button",
            "id": "1003"
        },
        "volume": {
            "input_type": "encoder",
            "id": "1001"
        }
    }
}
"""
