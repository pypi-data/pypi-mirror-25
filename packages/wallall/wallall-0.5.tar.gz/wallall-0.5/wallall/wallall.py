#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
wallall by drbytes - A quickly thrown togheter WallAll Python library
It's stable but that's about it.. it's primary raison d'etre is to integrate it into HomeAssistant
Published under the APACHE2 license - See LICENSE file for more details.

'''
import json
import logging
import os
import platform
import sys
import socket
if sys.version_info[0] > 2:
    import http.client as httplib
    import urllib.parse as urllib
else:
    import httplib
    import urllib
logger = logging.getLogger('wallall')
if platform.system() == 'Windows':
    USER_HOME = 'USERPROFILE'
else:
    USER_HOME = 'HOME'

__version__ = '0.5'
class WallAllCtx(object):
    """The WallAllCtx class"""
    def __init__(self, host):
        """The host should be set as IP:PORT"""
        self._host = host
    @property
    def name(self):
        """ Gets the name of the WallAll Instance """
        return self._name
    @name.setter
    def name(self, value):
        """ Sets the WallAll name """
        self._name = value
    @property
    def brightness(self):
        """ Gets the current brightness level 1..254 """
        self._brightness = self.getStuff("/BRIGHT")
        return self._brightness
    @brightness.setter
    def brightness(self, value):
        """ Sets the brightness 1..254. Beware that a setting of 0 is not allowed, see android reference regarding screen brightness write settings"""
        self._brightness = value;
        self.getStuff("/SETBRIGHT?what="+ str(value))
    @property
    def volume(self):
        """ Gets the current level of volume, this is for the media stream """
        self._volume = self.getStuff("/VOLUME")
        return self._volume
    @property
    def battery(self):
        """ Gets the current battery level in percentage """
        self._battery = self.getStuff("/BATTERY")
        return self._battery
    @property
    def lightsensor(self):
        """ Gets the value of the lightsensor, in lux """
        self._lux = self.getStuff("/LIGHT")
        return self._lux
    @property
    def soundsensor(self):
        """ Gets the value of the soundsensor, not in db but amplitude. Correct the value to db, its device specific """
        self._dblevel = self.getStuff("/SOUND")
        return self._dblevel
    def volumeUp(self):
        """ Increment the volume  """
        self.getStuff("/VOLUMEUP")

    def volumeDown(self):
        """ Decreases the volume """
        self.getStuff("/VOLUMEDOWN")
    def speak(self, what):
        """ Uses TTS to output text using the WallAll instance """
        return self.getStuff("/SAY?what=" +  urllib.quote(what))
    def play(self, what):
        """ Plays a locally stored media file on the WallAll instance, use the full path """
        return self.getStuff("/PLAY?what=" + urllib.quote(what))
    def image(self, what):
        """ Grabs an image off the camera """
        return self.getStuff("/IMAGE?what=" + urllib.quote(what))
    def getStuff(self, command):
        """ Performs the actual get on the WallAll instance """
        conn = httplib.HTTPConnection(self._host)
        conn.request("GET", command)
        return conn.getresponse().read()
