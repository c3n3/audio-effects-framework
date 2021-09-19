from aef import files
from aef import logger
from aef.logger import Logger
from aef.settings import GS_temp
import os

# Loop over all the modules inside the files folder, and output to temp
class DefaultFiles():
    @staticmethod
    def init():
        for file in files.files:
            print("outputing ", file.name)
            try:
                os.makedirs(os.path.dirname(GS_temp(file.name)), exist_ok=True)
                f = open(GS_temp(file.name), "w")
                f.write(file.file)
                f.close()
            except:
                Logger.log("Bad default file", "ERROR")
