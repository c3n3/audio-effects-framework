import re

def LOG(x):
    print(x)

class PdParser():
    def __init__(self):
        self.subPatchIndex = 0
        pass

    def makeCanvasName(self, fileName):
        # Remove funky stuff
        new = fileName.replace(" ", "_")
        new = new.replace(".", "_")
        new = new.replace(";", "_")
        new = new.replace("/", "_")
        new = new.replace("\\", "_")
        return new

    def parseFile(self, file):
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

        # TODO: Should parse all other things here as well

        # Make the patch somewhat neat by adding virtical offsets
        contents += f"#X restore 100 {self.subPatchIndex * 25 + 100} pd {newCanvasName};\n"

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
            self.subPatchIndex += 1

        # Now that all the files have been attached, we need to add the DAC~ and ADC~

        adcIndex = self.subPatchIndex
        resultantFile += "#X obj 100 75 adc~;\n"

        dacIndex = adcIndex + 1
        resultantFile += f"#X obj 100 {self.subPatchIndex*25 + 100} dac~;\n"

        # 1st index needs to link to the adc not another canvas
        for i in range(1, self.subPatchIndex):
            # Link 0th output of i-1 to 0th  input of i
            resultantFile += f"#X connect {i-1} 0 {i} 0;\n"

        resultantFile += f"#X connect {adcIndex} 0 {0} 0;\n"
        resultantFile += f"#X connect {self.subPatchIndex-1} 0 {dacIndex} 0;\n"


        f = open(outputFile, "w")
        f.write(resultantFile)        
        f.close()

parser = PdParser()

parser.parseFiles(["Viola.pd", "Delay.pd"], "master.pd")
