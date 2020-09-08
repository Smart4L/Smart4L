#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"
"""
Python module for DHT11 temps sensor
pip3 install Adafruit_DHT
"""
from random import randint
from utils import SensorInterface
try:
    import Adafruit_DHT
except ImportError:
    print("--- Adafruit_DHT import failed ---")

class DHT11(SensorInterface):
    def __init__(self, pin=None):
        self.DHT11_pin = pin
        if pin is not None:
            self.sensor = Adafruit_DHT.DHT11

    def measure(self):
        if self.DHT11_pin is None:
            temperature = 15+randint(0,20)
            humidity = 80+randint(0,20)
        else:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.DHT11_pin)
            # {"temperature":{0:0.1f}  ,"Humidity":{1:0.1f}}
        if humidity is not None and temperature is not None:
            return {"temperature": temperature  ,"humidity": humidity}
        else:
            return "DHT11_MEASURE_ERROR"

    def stop(self):
        pass

    def __str__(self):
        return "DHT11"

    def __repr__(self):
        return str(self)





