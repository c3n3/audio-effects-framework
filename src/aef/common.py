import subprocess as sp

def runSilent(command):
    return sp.run(command, stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=True)
