import re
import os
from aef.settings import GlobalSettings
class RoutingHook():
    def __init__(self, index, file, routeId):
        # The last in the list will have a ; we can get rid of it
        routeId = routeId.replace(";", '')
        self.index = index
        self.file = file
        self.routeId = routeId
        split = self.routeId.split('-')
        print("Split: ", split)
        self.min = 0
        self.increment = 0
        self.max = 0
        self.current = 0
        self.name = split[0]
        if (len(split) > 4):
            try:
                self.min = float(split[1])
                self.increment = abs(float(split[2]))
                self.max = float(split[3])
                self.current = float(split[4])
            except:
                print("ERROR, invalid routing range in file {}: ".format(file), routeId)

    def up(self):
        self.current = self.current + self.increment
        if (self.current > self.max):
            self.current = self.max

    def down(self):
        self.current = self.current - self.increment
        if (self.current < self.min):
            self.current = self.min

    def print(self):
        print("Index: ", self.index)
        print("file: ", self.file)
        print("routeId: ", self.routeId)
        print("start: ", self.current)
        print("increment: ", self.increment)
        print("max: ", self.max)
        print("min: ", self.min)

class PuredataFile():
    """Represents a single PD file
    """
    routingHooks = []

    def __init__(self, name, initHooks=False):
        """Init starts parsing PD. need to just read to figure out

        Args:
            name (str): Name of file
        """
        self.stubName = re.sub(".*/([^/]*?)\.pd", "\\1", name)
        self.connects = ""
        self.objects = ""
        self.objectCount = 0
        self.inputObject = -1
        self.outputObject = -1
        self.startIndex = 0
        self.routingObjects = []
        try:
            f = open(name, 'r')
            string = f.read()
            f.close
        except:
            return
        matches = re.findall("([^\\s](.|\\s)*?;)", string)

        obj = re.compile("#X")
        connect = re.compile('#X connect')
        outObj = re.compile("1.0002")
        inObj = re.compile("1.0001")
        routingObject = re.compile("(#X obj [0-9]* [0-9]* route) (.*)")
        onConnects = False
        for index, m in enumerate(matches):
            line = m[0]
            if (re.search(routingObject, line)):
                signals = re.match(routingObject, line)[2].split(" ")
                for i in range(0, len(signals)):
                    signals[i] = "__" + self.stubName + "__" + signals[i]
                    if (initHooks):
                        # We save all routing hooks so we can generate commands later
                        PuredataFile.routingHooks.append(RoutingHook(index - 1, name, signals[i]))
                #Store all the routing objects
                self.routingObjects.append(index - 1)
                line = re.sub(routingObject, "\\1 {}".format(" ".join(signals)), line)
            if (onConnects or re.search(connect, line)): # we have a connect here
                onConnects = True
                self.connects += line + "\n"
            elif (re.search(obj, line)):
                self.objectCount += 1
                self.objects += line + "\n"
            if (not onConnects and re.search(inObj, line)):
                self.inputObject = index - 1 # - 1 because of th ecanvas starting object
            elif (not onConnects and re.search(outObj, line)):
                self.outputObject = index - 1 # same as above

    def offset(self, startIndex):
        """Used to offset a files contained indices

        Args:
            startIndex (int): the index to start offseting from

        Returns:
            int: the last index after the offset
        """
        self.startIndex = startIndex
        self.inputObject += startIndex
        self.outputObject += startIndex
        for i in range(0, self.objectCount):
            self.restringConnects(i, i + startIndex)
        self.cleanConnects()
        return self.startIndex + self.objectCount

    def cleanConnects(self):
        """Connects are labelled so that we can make multiple passes over the file. This cleans them
        """
        self.connects = re.sub(r"\[`", '', self.connects)

    def restringConnects(self, objectNumber, replace):
        """Restrings all the connects to their new number

        Args:
            objectNumber (int): The object number
            replace (int): The replacement number
        """
        self.connects = re.sub("((t ){}( )|( ){}( \\d;))".format(objectNumber, objectNumber), "\\2\\4[`{}\\3\\5".format(replace), self.connects)

#need to convert to a non reparsing format and keep all the files
class PuredataParser():
    """Static class handles all PD parsing
    """
    @staticmethod
    def parse(fileNames, dir1, globalFiles, dir2, outPath):
        """Parses all the files given

        Args:
            fileNames (list<str>): A list of files to parse
            dir1 (str): Directory for non global files
            globalFiles (list<str>): List of global files to parse
            dir2 (str): global dir
            outPath (str): file to output
        """
        files = []
        index = 0
        result = "#N canvas 2521 143 995 666 12;"
        for file in fileNames:
            result += "\n"
            files.append(PuredataFile(dir1 + file, outPath == None))
            index = files[len(files) - 1].offset(index)
            result += files[len(files) - 1].objects
        for file in globalFiles:
            result += "\n"
            files.append(PuredataFile(dir2 + file))
            index = files[len(files) - 1].offset(index)
            result += files[len(files) - 1].objects

        result += "#X obj 0 0 adc~;\n"
        result += "#X obj 0 0 dac~;\n"

        result += "#X msg 378 115 \n; pd dsp 1 \n;;\n#X obj 376 53 loadbang;\n"
        result += "#X obj 519 62 netreceive 2999;"
        adcIndex = index
        dacIndex = index + 1
        netObj = index + 4
        result += "#X connect {} 0 {} 0;\n".format(adcIndex, files[0].inputObject)
        result += "#X connect {} 1 {} 0;\n".format(adcIndex, files[0].inputObject)
        result += "#X connect {} 0 {} 0;\n".format(files[len(files) - 1].outputObject, dacIndex)
        result += "#X connect {} 0 {} 1;\n".format(files[len(files) - 1].outputObject, dacIndex)
        result += "#X connect {} 0 {} 0;\n".format(index + 3, index + 2)
        for file in files:
            result += file.connects + "\n"
        for file in files:
            for route in file.routingObjects:
                result += "#X connect {} 0 {} 0;\n".format(netObj, route + file.startIndex)
        for index, file in enumerate(files):
            if (index == 0):
                continue
            result += "#X connect {} 0 {} 0;\n".format(files[index - 1].outputObject, files[index].inputObject)
        if (outPath != None):
            f = open(outPath, "w")
            f.write(result)
            f.close()

