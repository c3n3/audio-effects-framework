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

import re
from time import sleep
from aitpi.mirrored_json import MirroredJson
from aef.constants import Constants
from threading import Thread
from aef.log import *
from aef.settings import GlobalSettings


class GlobalObject:
    def __init__(self, find, replaceFun):
        self.find = find
        self.replaceFun = replaceFun
        self.stubName = ""

    def findAndReplace(self, file, contents):
        self.stubName = re.sub(".*/([^/]*?)\.pd", "\\1", file)
        self.stubName = self.stubName.replace(".", "")
        self.stubName = self.stubName.replace("pd", "")
        replace = self.replaceFun(self.stubName)
        return re.sub(self.find, replace, contents)


class RoutingHook:
    hookCache = None
    editCache = False
    cacheThread = None

    @staticmethod
    def initCache():
        if RoutingHook.hookCache is None:
            RoutingHook.hookCache = MirroredJson(
                f"{GlobalSettings.settings['temp_dir']}/hook.cache.json", autosave=False
            )
            RoutingHook.cacheThread = Thread(
                target=RoutingHook.updateCacheThread, daemon=True
            )
            RoutingHook.cacheThread.start()

    @staticmethod
    def updateCacheThread():
        while True:
            # Only save when there is an edit
            # TODO: Maybe we need a mutex here, probably not
            if RoutingHook.editCache:
                RoutingHook.hookCache.save()
            RoutingHook.editCache = False
            # 5 second delay should be good
            sleep(5)

    def __init__(self, string):
        self.low = 0
        self.high = 0
        self.increment = 0
        self.start = 0
        self.routeId = string
        split = string.split("-")

        if len(split) < 4:
            ilog(f"Not enough arguments in routing object '{string}'")
            self.name = None
            return
        self.name = split[0]

        try:
            self.min = float(split[1])
            self.increment = abs(float(split[2]))
            self.max = float(split[3])
        except:
            elog("Invalid route arguements")
        try:
            self.current = float(split[4])
        except:
            self.current = (self.max + self.min) / 2
        if self.name in RoutingHook.hookCache.keys():
            self.current = self.hookCache[self.name]
        else:
            # TODO: Potential cache bloat from old entries
            RoutingHook.hookCache[self.name] = self.current

    def up(self):
        self.current = self.current + self.increment
        if self.current > self.max:
            self.current = self.max
        RoutingHook.hookCache[self.name] = self.current
        RoutingHook.editCache = True

    def down(self):
        self.current = self.current - self.increment
        if self.current < self.min:
            self.current = self.min
        RoutingHook.hookCache[self.name] = self.current
        RoutingHook.editCache = True


class PdParser:
    hooks = {}
    filesToHooks = {}
    files = {}
    globalObjects = {
        # Replace all names of '__' routing objects so that it is simple to identify
        "route": GlobalObject(
            find="(#X obj [0-9]+? [0-9]+? route) (__[^\s]*?;)",
            replaceFun="\\1 {}\\2".format,
        )
    }

    def __init__(self):
        RoutingHook.initCache()
        self.subPatchIndex = 0

    def addHook(self, string, file):
        hook = RoutingHook(string)
        if hook.routeId != None and hook.name != None:
            PdParser.hooks[hook.name] = hook
            simpleName = re.sub(".*/([^/]*?)", "\\1", file)
            if simpleName not in PdParser.filesToHooks:
                PdParser.filesToHooks[simpleName] = []
            PdParser.filesToHooks[simpleName].append(hook)

    def makeCanvasName(self, fileName):
        # Remove funky stuff
        new = fileName.replace(" ", "_")
        new = new.replace(".", "_")
        new = new.replace(";", "_")
        new = new.replace("/", "_")
        new = new.replace("\\", "_")
        return new

    def parseFile(self, file):
        # Use cached results
        if file in PdParser.files:
            return PdParser.files[file]

        f = None
        try:
            f = open(file)
        except:
            elog("Invalid File " + str(file))
            return None

        contents = f.read()
        f.close()
        newCanvasName = self.makeCanvasName(file.split("/").pop())

        # First we need to modify the name of the main canvas so as to make it a subcanvas
        # Last item in list is text size, we will force that to be 12
        canvas = re.compile("(#N canvas [0-9]+? [0-9]+? [0-9]+? [0-9]+?) [0-9]+?;")

        # Give canvas a new name
        contents = re.sub(canvas, f"\\1 {newCanvasName} 12;", contents)

        for key, globalObject in PdParser.globalObjects.items():
            contents = globalObject.findAndReplace(file, contents)

        # Find all routing hooks:
        regex = f"#X obj [0-9]+? [0-9]+? route ({PdParser.globalObjects['route'].stubName}__[^\s]*?);"
        hook = re.compile(regex)

        results = re.findall(hook, contents)
        for res in results:
            self.addHook(res, file)

        # Cache results
        PdParser.files[file] = contents
        return contents

    def parseFiles(self, files, outputFile):
        """ Parse files and link in the order presented

        Args:
            files (list): list of files to parse
            outputFile (str): String of the output file path/name
        """
        self.subPatchIndex = 0
        resultantFile = "#N canvas 201 290 450 300 12;\n"
        for file in files:
            result = self.parseFile(file)
            if result is None:
                continue
            resultantFile += result

            # End of canvas
            resultantFile += f"#X restore 100 {self.subPatchIndex * 25 + 100} pd {self.makeCanvasName(file.split('/').pop())};\n"

            self.subPatchIndex += 1

        # Now that all the files have been attached, we need to add the DAC~ and ADC~

        adcIndex = self.subPatchIndex
        resultantFile += "#X obj 100 75 adc~;\n"

        dacIndex = adcIndex + 1
        resultantFile += f"#X obj 100 {self.subPatchIndex*25 + 100} dac~;\n"

        netrecvIndex = dacIndex + 1
        resultantFile += f"#X obj 200 75 netreceive 2999;\n"

        # Since we loop through 1 -> range, link first netrecv here:
        resultantFile += f"#X connect {netrecvIndex} 0 {0} 2;\n"

        # 1st index needs to link to the adc not another canvas
        for i in range(1, self.subPatchIndex):
            # Link 0th output of i-1 to 0th  input of i
            # Left~
            resultantFile += f"#X connect {i-1} 0 {i} 0;\n"

            # Right~
            resultantFile += f"#X connect {i-1} 1 {i} 1;\n"

            # Netreceive
            resultantFile += f"#X connect {netrecvIndex} 0 {i} 2;\n"

        # Link the ADC and DAC
        resultantFile += f"#X connect {adcIndex} 0 {0} 0;\n"
        resultantFile += f"#X connect {adcIndex} 1 {0} 1;\n"

        resultantFile += f"#X connect {self.subPatchIndex-1} 0 {dacIndex} 0;\n"
        resultantFile += f"#X connect {self.subPatchIndex-1} 1 {dacIndex} 1;\n"

        if outputFile is not None:
            f = open(outputFile, "w")
            f.write(resultantFile)
            f.close()
