#!/usr/bin/python3
import aef
import aitpi
import sys

effects = "../default_effects/"
presets = "../default_presets/"
recordings = "./recordings/"

def init():
    print("args", sys.argv)
    aef.run(effects, recordings, presets, sys.argv)

init()
aitpi.initInput('input.json')

try:
    while (True):
            name = input("Name: ")
            value = input("Value: ")
            aef.changeLink(name, value)
except:
    print("Shutting down")

aef.shutdown()
