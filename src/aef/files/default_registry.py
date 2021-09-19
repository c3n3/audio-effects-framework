from aef.constants import Constants
name = Constants.DEFAULT_COMMAND_REGISTRY
file="""
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
    },
    "recordings": {
        "Recording_0.wav": {
            "id": 1003,
            "input_type": "button",
            "path": "/git/audio-effects-framework/src/aef/../../recordings/"
        }
    },
    "effects": {
        "Delay.pd": {
            "id": 1005,
            "input_type": "button",
            "path": "/git/audio-effects-framework/src/aef/../../default_effects/"
        },
        "Synth.pd": {
            "id": 1005,
            "input_type": "button",
            "path": "/git/audio-effects-framework/src/aef/../../default_effects/"
        },
        "Distortion.pd": {
            "id": 1005,
            "input_type": "button",
            "path": "/git/audio-effects-framework/src/aef/../../default_effects/"
        },
        "Fuzz.pd": {
            "id": 1005,
            "input_type": "button",
            "path": "/git/audio-effects-framework/src/aef/../../default_effects/"
        },
        "Viola.pd": {
            "id": 1005,
            "input_type": "button",
            "path": "/git/audio-effects-framework/src/aef/../../default_effects/"
        },
        "Tremolo.pd": {
            "id": 1005,
            "input_type": "button",
            "path": "/git/audio-effects-framework/src/aef/../../default_effects/"
        }
    },
    "presets": {
        "21Guns.pre": {
            "id": 1002,
            "input_type": "button",
            "path": "/git/audio-effects-framework/src/aef/../../default_presets/"
        }
    }
}
"""