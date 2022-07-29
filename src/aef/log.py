import os
import inspect
from aef.settings import GlobalSettings

loglevels = {"Debug": 0, "Info": 1, "Warning": 2, "Error": 3}

def logLocation():
    return GlobalSettings.settings['log_folder']

def logLevel():
    return GlobalSettings.settings['log_level']

def _report(level, infoFromUpstack, *args):
    print(level, logLevel(), loglevels)
    if loglevels[level] >= loglevels[logLevel()]:
        loc = inspect.stack()[infoFromUpstack]
        file = os.path.abspath(loc.filename)
        lineno = loc.lineno
        prefix = f"{file}:{lineno}::{level}:"
        if logLocation() == '':
            print(prefix, *args)
        elif os.path.exists(logLocation()):
            with open(f"{logLocation()}/{level}.log", 'a') as f:
                out = prefix + " " + " ".join(args) + "\n"
                f.write(out)
        else:
            print("AEF::Error: Invalid log location. No logs will be recorded.")

def _output(level, *args):
    # Up stack 4 times (including 0) for elog, _output, and _report
    _report(level, 3, *args)

def dlog(*args):
    _output("Debug", *args)

def ilog(*args):
    _output("Info", *args)

def wlog(*args):
    _output("Warning", *args)

def elog(*args):
    _output("Error", *args)
