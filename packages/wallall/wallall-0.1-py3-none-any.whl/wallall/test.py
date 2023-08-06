#!/usr/bin/python
# -*- coding: utf-8 -*-

import wallall

classinstance = wallall.WallAll("192.168.1.163:8080")
print(classinstance.soundsensor)
print(classinstance.lightsensor)
print(classinstance.brightness)
print(classinstance.volume)
print(classinstance.battery)
classinstance.volumeDown()

classinstance.speak("Fuck yeah, this shit works!")