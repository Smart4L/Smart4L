#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"
"""
Python module for HC-SR04 UltraSon Sensor
https://raspberrypi-tutorials.fr/utilisation-dun-capteur-de-distance-raspberry-pi-capteur-ultrasonique-hc-sr04/
"""
# standard library
import os
import sys
from utils import SensorInterface
from random import randint
import time
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("--- RPI import failed ---")

class HCSR04(SensorInterface):
    def __init__(self, echo_pin=None, trigger_pin=None):
        #GPIO.setmode(GPIO.BCM)
        self.GPIO_ECHO = echo_pin
        self.GPIO_TRIGGER = trigger_pin
        try:
            GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
            GPIO.setup(GPIO_ECHO, GPIO.IN)
        except:
            pass

    def measure(self):
        if self.GPIO_ECHO is None:
            return randint(1,4)

        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        #print ("Measured Distance = %.1f cm" % dist)
        return distance

    def stop(self):
        try:
            GPIO.cleanup()
        except:
            pass
