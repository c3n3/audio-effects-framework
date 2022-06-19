import re

def LOG(x):
    print(x)

class GlobalObject():
    def __init__(self, find, replaceFun):
        self.find = find
        self.replaceFun = replaceFun

    def findAndReplace(self, file, contents):
        stubName = re.sub(".*/([^/]*?)\.pd", "\\1", file)
        stubName = stubName.replace(".", "")
        stubName = stubName.replace("pd", "")
        replace = self.replaceFun(stubName)
        return re.sub(self.find, replace, contents)

class RoutingHook():
    def __init__(self, string):
        self.low = 0
        self.high = 0
        self.increment = 0
        self.start = 0
        self.routeId = string        
        split = string.split("-")

        if (len(split) < 4):
            LOG("Not enough arguments in routing object")
            self.name = None
            return

        try:
            self.min = float(split[1])
            self.increment = abs(float(split[2]))
            self.max = float(split[3])
        except:
            LOG("Invalid route arguements")
        try:
            self.current = float(split[4])
        except:
            self.current = (self.max + self.min) / 2

    def up(self):
        self.current = self.current + self.increment
        if (self.current > self.max):
            self.current = self.max

    def down(self):
        self.current = self.current - self.increment
        if (self.current < self.min):
            self.current = self.min


class PdParser():
    hooks = {}
    files = {}
    globalObjects = [
        # Replace all names of '__' routing objects so that it is simple to identify
        GlobalObject(
            find="(#X obj [0-9]+? [0-9]+? route) (__[^\s]*?;)",
            replaceFun="\\1 {}\\2".format
        )
    ]


    def __init__(self):
        self.subPatchIndex = 0
        pass

    def addHook(self, string):
        hook = RoutingHook(string)
        if (hook.routeId != None):
            PdParser.hooks[hook.routeId] = hook

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
        if (file in  PdParser.files):
            return PdParser.files[file]

        f = None
        try:
            f = open(file)
        except:
            LOG("Invalid File ")
            return None



        contents = f.read()
        f.close()
        newCanvasName = self.makeCanvasName(file.split('/').pop())

        # First we need to modify the name of the main canvas so as to make it a subcanvas      
        # Last item in list is text size, we will force that to be 12
        canvas = re.compile("(#N canvas [0-9]+? [0-9]+? [0-9]+? [0-9]+?) [0-9]+?;")

        # Give canvas a new name
        contents = re.sub(canvas, f"\\1 {newCanvasName} 12;", contents)

        for globalObject in PdParser.globalObjects:
            contents = globalObject.findAndReplace(file, contents)

        # Find all routing hooks:
        hook = re.compile("#X obj [0-9]+? [0-9]+? route (__[^\s]*?);")

        results = re.findall(hook, contents)

        for res in results:
            self.addHook(res)

        # TODO: rename global variables

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
            resultantFile += self.parseFile(file)

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


        f = open(outputFile, "w")
        f.write(resultantFile)        
        f.close()

parser = PdParser()

parser.parseFiles(["Viola.pd", "Delay.pd"], "master.pd")
