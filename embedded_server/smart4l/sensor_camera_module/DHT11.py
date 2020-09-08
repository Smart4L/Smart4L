#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"
"""
Python module for DHT11 temps sensor
"""
from random import randint
from utils import SensorInterface


class DHT11(SensorInterface):
    def __init__(self):
        pass

    def measure(self):
        return randint(100,999)

    def stop(self):
        pass

    def __str__(self):
        return "DHT11"

    def __repr__(self):
        return str(self)
