#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"
"""
Python module for DS18B20 temps sensor
"""

import os  # standard library
import sys
from utils import SensorInterface


# /etc/modules
# w1-therm
# w1-gpio pullup=1
# i2c-dev
# i2c-bcm2708
# spi-bcm2708
# snd-bcm2835

# /etc/modprobe.d/raspi-blacklist.conf
# blacklist spi-bcm2708
# blacklist i2c-bcm2708

# /boot/config.txt
# dtoverlay=w1-gpio

class DS18B20(SensorInterface):
	def __init__(self, id=None):
		self.id_sonde = id

	def measure(self):
	    if self.id_sonde is None:
	    	return 42
	    return str(float(open("/sys/bus/w1/devices/%s/w1_slave" % self.id_sonde).read().split()[-1][2:])/1000)

	def stop(self):
		pass
