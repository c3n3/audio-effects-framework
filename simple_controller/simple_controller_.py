import aef
import aitpi

effects = "../default_effects/"
presets = "../default_presets/"
recordings = "./recordings/"

def init():
    aef.run(effects, recordings, presets)


def checkName(name):
    return True # return if valid

def checkValue(name):
    return True # return if valid

init()
aitpi.initInput('input.json')

try:
    while (True):
            name = input("Name: ")
            if (not checkName(name)):
                print("Invalid name")
                continue

            value = input("Value: ")

            if (not checkValue(value)):
                print("Invalid value")
                continue

            aef.changeLink(name, value)
except:
    print("Shutting down")

aef.shutdown()
