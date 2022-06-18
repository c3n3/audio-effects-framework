# Audio effects framework
The audio effects framework is a python module that allows for easy use of audio effects created in puredata (https://puredata.info).

## Use
The audio effect framework was built upon the AITPI system (https://github.com/c3n3/AITPI). This system is used in order to control the application and modification of the audio effects framework. It allows inputs (currently supported keyboard input, raspberry pi GPIO buttons, and raspberry pi GPIO encoders) to be written in JSON to control what audio effects are applied in real time. These inputs are to be expanded over time.

### Running

In order to run the aef:

```
import aef
import aitpi

# Any application setup...

aef.run(effectsFolder, recordingsFolder, presetsFolder, sys.argv)
inputJson = os.path.join(dirname, 'your_input.json')
aitpi.initInput(inputJson)
```

And when done:

```
aef.shutdown()
```

Aef will automatically link into the jack audio system and will automatically start receiving input.

NOTE: Currently the setup is to use Qjackctl with a preset named 'guitar-module'. This setup must be done before hand. This will be ammended in the future.


### Setting up AITPI

See https://github.com/c3n3/AITPI. The possible commands to link to are all listed out in the temp folder.

>> NOTE: wherever you run the aef, it will create a ./temp/ folder in the local directory. This will contain all temporary files such as recordings, puredata temp files, and the command registry.

Currently you can retrieve these commands by calling:

```
aef.getCommands()
```

You can also change the input links on the fly by calling:

```
aef.changeLink(inputName, newCommandToLink)
```

### Presets

You can create presets that specify multiple audio effects to apply at once. These are simply text files that list out the names of all effects. You can see examples of these in the default_presets folder. These will show up automatically in the command registry if they are put into the 'presetsFolder' (specified in `aef.run`).


### Effects

You can create new puredata patches in input them into the 'effectsFolder' (specified in `aef.run`). These must follow a specific format in puredata in order to be linked properly. TODO: Specify puredata format rules.


### Recordings

Recordings are created with the 'save' command. It will save whatever was the last 'record' audio into the recordings folder (as specified in `aef.run`). This will then be added to the command list in so that you can replay the recording with a keystroke (based on AITPI).

