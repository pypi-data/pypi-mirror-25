#!/usr/bin/python
# -*- coding: utf-8 -*-

import wallall

classinstance = wallall.WallAll("10.8.0.2:8080")
print(classinstance.soundsensor)
print(classinstance.lightsensor)
print(classinstance.brightness)
print(classinstance.volume)
print(classinstance.battery)

msg = classinstance.image

import pickle
with open("bytesfile", "wb") as mypicklefile:
    pickle.dump(msg, mypicklefile)
